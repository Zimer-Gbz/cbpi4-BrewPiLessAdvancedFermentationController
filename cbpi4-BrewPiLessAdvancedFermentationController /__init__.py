import logging
import time
from cbpi.api import *

class PID:
    def __init__(self, Kp, Ki, Kd, sample_time):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.sample_time = sample_time
        self.clear()

    def clear(self):
        self.last_error = 0
        self.int_error = 0
        self.last_time = None

    def compute(self, setpoint, input_val):
        now = time.time()
        error = setpoint - input_val
        delta_time = self.sample_time if self.last_time is None else now - self.last_time
        self.int_error += error * delta_time
        d_error = (error - self.last_error) / delta_time if delta_time > 0 else 0
        output = self.Kp * error + self.Ki * self.int_error + self.Kd * d_error
        self.last_error, self.last_time = error, now
        return output


@cbpi.actor
class FridgeCompressor(AktorBase):
    def on(self, **kwargs): 
        self.api.switch_on(self.id)

    def off(self, **kwargs): 
        self.api.switch_off(self.id)


@cbpi.fermenter_controller
class BrewPiLessAdvancedFermentationController(ControlBase):
    beer_sensor = Property.Sensor("Sensor de Fermentador", description="Sonda na cerveja")
    fridge_sensor = Property.Sensor("Sensor da Câmara", description="Sonda na câmara")
    heater = Property.Actor("Aquecedor", description="Atuador de aquecimento")
    cooler = Property.Actor("Resfriador", description="Atuador de refrigeração")
    target = Property.Number("Setpoint de Fermentação", True, 20, description="Temperatura alvo da cerveja (°C)")

    kp = Property.Number("Kp", True, 10.0)
    ki = Property.Number("Ki", True, 0.0)
    kd = Property.Number("Kd", True, 80.0)
    cycle_time = Property.Number("Ciclo de Controle (seg)", True, 60)
    min_on_time = Property.Number("Tempo Mínimo Ligado (seg)", True, 180)
    min_off_time = Property.Number("Tempo Mínimo Desligado (seg)", True, 300)
    dead_time = Property.Number("Dead Time (seg)", True, 300)
    freeze_protect_temp = Property.Number("Limite Anti-Congelamento (°C)", True, 1.0)

    STATE_IDLE = "IDLE"
    STATE_COOLING = "COOLING"
    STATE_HEATING = "HEATING"
    STATE_WAIT = "WAIT"
    STATE_ERROR = "ERROR"

    def init(self):
        self.pid = PID(self.kp, self.ki, self.kd, self.cycle_time)
        self.state = self.STATE_IDLE
        self.state_since = time.time()
        self.last_cool = None
        self.last_heat = None
        self.wait_start = None

    @property
    def beer_temp(self):
        return self.get_sensor_value(self.beer_sensor)

    @property
    def fridge_temp(self):
        return self.get_sensor_value(self.fridge_sensor)

    def enter_state(self, new_state):
        self.state = new_state
        self.state_since = time.time()
        self.notify(f"Estado alterado para {new_state}")

    def can_turn_on_cooler(self):
        now = time.time()
        if self.beer_temp is None:
            return False
        if self.beer_temp <= self.freeze_protect_temp:
            self.notify("Proteção anti-congelamento ativada, não ligando resfriador")
            return False
        if self.last_cool is None:
            return True
        return (now - self.last_cool) >= self.min_off_time

    def can_turn_on_heater(self):
        now = time.time()
        if self.last_heat is None:
            return True
        return (now - self.last_heat) >= self.min_off_time

    def control(self):
        beer = self.beer_temp
        fridge = self.fridge_temp
        target = self.target

        if beer is None or fridge is None:
            self.enter_state(self.STATE_ERROR)
            self.notify("Erro: sensores desconectados ou inválidos")
            self.api.switch_off(self.cooler)
            self.api.switch_off(self.heater)
            return

        fridge_setpoint = self.pid.compute(target, beer)
        self.notify(f"Setpoint da câmara calculado: {fridge_setpoint:.2f}°C")

        now = time.time()
        elapsed = now - self.state_since

        if self.state == self.STATE_IDLE:
            if fridge > fridge_setpoint + 0.5 and self.can_turn_on_cooler():
                self.api.switch_on(self.cooler)
                self.enter_state(self.STATE_COOLING)
                self.last_cool = now
                self.last_heat = None
                self.api.switch_off(self.heater)
            elif fridge < fridge_setpoint - 0.5 and self.can_turn_on_heater():
                self.api.switch_on(self.heater)
                self.enter_state(self.STATE_HEATING)
                self.last_heat = now
                self.last_cool = None
                self.api.switch_off(self.cooler)

        elif self.state == self.STATE_COOLING:
            if fridge <= fridge_setpoint or elapsed >= self.min_on_time:
                self.api.switch_off(self.cooler)
                self.enter_state(self.STATE_WAIT)
                self.wait_start = now

        elif self.state == self.STATE_HEATING:
            if fridge >= fridge_setpoint or elapsed >= self.min_on_time:
                self.api.switch_off(self.heater)
                self.enter_state(self.STATE_WAIT)
                self.wait_start = now

        elif self.state == self.STATE_WAIT:
            if (now - self.wait_start) >= self.dead_time:
                self.enter_state(self.STATE_IDLE)

        elif self.state == self.STATE_ERROR:
            self.api.switch_off(self.cooler)
            self.api.switch_off(self.heater)
            if beer is not None and fridge is not None:
                self.enter_state(self.STATE_IDLE)

    def run(self):
        while self.is_running():
            self.control()
            self.sleep(int(self.cycle_time))

# Registro do plugin no CraftBeerPi
def setup(cbpi):
    cbpi.plugin.register("BrewPiLessAdvancedFermentationController", BrewPiLessAdvancedFermentationController)
