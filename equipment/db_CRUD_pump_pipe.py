from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from db_CRUD_tank import BaseEquipment, DatabaseConnection  # Импортируем из предыдущего файла



@dataclass
class Pump:
    pump_id: Optional[int]
    pump_name: str
    pump_type: str
    volume: float
    flow: float
    time_out: float
    pressure: float
    temperature: float
    component_enterprise: str
    sub_id: int
    coordinate: str


class PumpCRUD(BaseEquipment):
    def create(self, data: Dict[str, Any]) -> int:
        with DatabaseConnection(self.db_path) as cursor:
            cursor.execute("""
                INSERT INTO Pump (
                    pump_name, pump_type, volume, flow, time_out,
                    pressure, temperature, component_enterprise,
                    sub_id, coordinate
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data['pump_name'], data['pump_type'], data['volume'],
                data['flow'], data['time_out'], data['pressure'],
                data['temperature'], data['component_enterprise'],
                data['sub_id'], data['coordinate']
            ))
            return cursor.lastrowid

    def read(self, id: int) -> Optional[Dict[str, Any]]:
        with DatabaseConnection(self.db_path) as cursor:
            cursor.execute("SELECT * FROM Pump WHERE pump_id = ?", (id,))
            row = cursor.fetchone()
            if row:
                return dict(row)
            return None

    def update(self, id: int, data: Dict[str, Any]) -> bool:
        with DatabaseConnection(self.db_path) as cursor:
            cursor.execute("""
                UPDATE Pump
                SET pump_name = ?, pump_type = ?, volume = ?,
                    flow = ?, time_out = ?, pressure = ?,
                    temperature = ?, component_enterprise = ?,
                    sub_id = ?, coordinate = ?
                WHERE pump_id = ?
            """, (
                data['pump_name'], data['pump_type'], data['volume'],
                data['flow'], data['time_out'], data['pressure'],
                data['temperature'], data['component_enterprise'],
                data['sub_id'], data['coordinate'], id
            ))
            return cursor.rowcount > 0

    def delete(self, id: int) -> bool:
        with DatabaseConnection(self.db_path) as cursor:
            cursor.execute("DELETE FROM Pump WHERE pump_id = ?", (id,))
            return cursor.rowcount > 0

    def list_all(self) -> List[Dict[str, Any]]:
        with DatabaseConnection(self.db_path) as cursor:
            cursor.execute("SELECT * FROM Pump")
            return [dict(row) for row in cursor.fetchall()]


@dataclass
class Pipeline:
    pipeline_id: Optional[int]
    pipeline_name: str
    diameter_category: str
    length_meters: float
    diameter_pipeline: float
    flow: float
    time_out: float
    pressure: float
    temperature: float
    component_enterprise: str
    sub_id: int
    coordinate: str


class PipelineCRUD(BaseEquipment):
    def create(self, data: Dict[str, Any]) -> int:
        with DatabaseConnection(self.db_path) as cursor:
            cursor.execute("""
                INSERT INTO Pipeline (
                    pipeline_name, diameter_category, length_meters,
                    diameter_pipeline, flow, time_out, pressure,
                    temperature, component_enterprise, sub_id, coordinate
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data['pipeline_name'], data['diameter_category'],
                data['length_meters'], data['diameter_pipeline'],
                data['flow'], data['time_out'], data['pressure'],
                data['temperature'], data['component_enterprise'],
                data['sub_id'], data['coordinate']
            ))
            return cursor.lastrowid

    def read(self, id: int) -> Optional[Dict[str, Any]]:
        with DatabaseConnection(self.db_path) as cursor:
            cursor.execute("SELECT * FROM Pipeline WHERE pipeline_id = ?", (id,))
            row = cursor.fetchone()
            if row:
                return dict(row)
            return None

    def update(self, id: int, data: Dict[str, Any]) -> bool:
        with DatabaseConnection(self.db_path) as cursor:
            cursor.execute("""
                UPDATE Pipeline
                SET pipeline_name = ?, diameter_category = ?, length_meters = ?,
                    diameter_pipeline = ?, flow = ?, time_out = ?,
                    pressure = ?, temperature = ?, component_enterprise = ?,
                    sub_id = ?, coordinate = ?
                WHERE pipeline_id = ?
            """, (
                data['pipeline_name'], data['diameter_category'],
                data['length_meters'], data['diameter_pipeline'],
                data['flow'], data['time_out'], data['pressure'],
                data['temperature'], data['component_enterprise'],
                data['sub_id'], data['coordinate'], id
            ))
            return cursor.rowcount > 0

    def delete(self, id: int) -> bool:
        with DatabaseConnection(self.db_path) as cursor:
            cursor.execute("DELETE FROM Pipeline WHERE pipeline_id = ?", (id,))
            return cursor.rowcount > 0

    def list_all(self) -> List[Dict[str, Any]]:
        with DatabaseConnection(self.db_path) as cursor:
            cursor.execute("SELECT * FROM Pipeline")
            return [dict(row) for row in cursor.fetchall()]


# Пример использования:
if __name__ == "__main__":
    # Пример работы с насосами
    pump_crud = PumpCRUD("db_eq.db")

    new_pump_data = {
        "pump_name": "Новый насос",
        "pump_type": "Центробежные герметичные",
        "volume": 50.0,
        "flow": 100.0,
        "time_out": 2.0,
        "pressure": 3.0,
        "temperature": 30.0,
        "component_enterprise": "Насосная станция 1",
        "sub_id": 1,
        "coordinate": "55.123456, 37.123456"
    }

    # Create pump
    new_pump_id = pump_crud.create(new_pump_data)
    print(f"Created new pump with ID: {new_pump_id}")

    # Пример работы с трубопроводами
    pipeline_crud = PipelineCRUD("db_eq.db")

    new_pipeline_data = {
        "pipeline_name": "Новый трубопровод",
        "diameter_category": "От 75 до 150 мм",
        "length_meters": 1000.0,
        "diameter_pipeline": 100.0,
        "flow": 50.0,
        "time_out": 1.5,
        "pressure": 2.5,
        "temperature": 25.0,
        "component_enterprise": "Установка 1",
        "sub_id": 1,
        "coordinate": "55.123456, 37.123456"
    }

    # Create pipeline
    new_pipeline_id = pipeline_crud.create(new_pipeline_data)
    print(f"Created new pipeline with ID: {new_pipeline_id}")