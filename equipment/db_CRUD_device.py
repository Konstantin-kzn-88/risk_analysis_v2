from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from db_CRUD_tank import BaseEquipment, DatabaseConnection  # Импортируем из первого файла


@dataclass
class TechnologicalDevice:
    device_id: Optional[int]
    device_name: str
    device_type: str
    volume: float
    degree_filling: float
    pressure: float
    temperature: float
    component_enterprise: str
    spill_square: float
    sub_id: int
    coordinate: str


class TechnologicalDeviceCRUD(BaseEquipment):
    def create(self, data: Dict[str, Any]) -> int:
        with DatabaseConnection(self.db_path) as cursor:
            cursor.execute("""
                INSERT INTO Technological_devices (
                    device_name, device_type, volume, degree_filling,
                    pressure, temperature, component_enterprise,
                    spill_square, sub_id, coordinate
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data['device_name'], data['device_type'], data['volume'],
                data['degree_filling'], data['pressure'], data['temperature'],
                data['component_enterprise'], data['spill_square'],
                data['sub_id'], data['coordinate']
            ))
            return cursor.lastrowid

    def read(self, id: int) -> Optional[Dict[str, Any]]:
        with DatabaseConnection(self.db_path) as cursor:
            cursor.execute("""
                SELECT * FROM Technological_devices WHERE device_id = ?
            """, (id,))
            row = cursor.fetchone()
            if row:
                return dict(row)
            return None

    def update(self, id: int, data: Dict[str, Any]) -> bool:
        with DatabaseConnection(self.db_path) as cursor:
            cursor.execute("""
                UPDATE Technological_devices
                SET device_name = ?, device_type = ?, volume = ?,
                    degree_filling = ?, pressure = ?, temperature = ?,
                    component_enterprise = ?, spill_square = ?,
                    sub_id = ?, coordinate = ?
                WHERE device_id = ?
            """, (
                data['device_name'], data['device_type'], data['volume'],
                data['degree_filling'], data['pressure'], data['temperature'],
                data['component_enterprise'], data['spill_square'],
                data['sub_id'], data['coordinate'], id
            ))
            return cursor.rowcount > 0

    def delete(self, id: int) -> bool:
        with DatabaseConnection(self.db_path) as cursor:
            cursor.execute("DELETE FROM Technological_devices WHERE device_id = ?", (id,))
            return cursor.rowcount > 0

    def list_all(self) -> List[Dict[str, Any]]:
        with DatabaseConnection(self.db_path) as cursor:
            cursor.execute("SELECT * FROM Technological_devices")
            return [dict(row) for row in cursor.fetchall()]


@dataclass
class TruckTank:
    truck_tank_id: Optional[int]
    truck_tank_name: str
    pressure_type: str
    volume: float
    degree_filling: float
    pressure: float
    temperature: float
    component_enterprise: str
    spill_square: float
    sub_id: int
    coordinate: str


class TruckTankCRUD(BaseEquipment):
    def create(self, data: Dict[str, Any]) -> int:
        with DatabaseConnection(self.db_path) as cursor:
            cursor.execute("""
                INSERT INTO Truck_tank (
                    truck_tank_name, pressure_type, volume, degree_filling,
                    pressure, temperature, component_enterprise,
                    spill_square, sub_id, coordinate
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data['truck_tank_name'], data['pressure_type'], data['volume'],
                data['degree_filling'], data['pressure'], data['temperature'],
                data['component_enterprise'], data['spill_square'],
                data['sub_id'], data['coordinate']
            ))
            return cursor.lastrowid

    def read(self, id: int) -> Optional[Dict[str, Any]]:
        with DatabaseConnection(self.db_path) as cursor:
            cursor.execute("SELECT * FROM Truck_tank WHERE truck_tank_id = ?", (id,))
            row = cursor.fetchone()
            if row:
                return dict(row)
            return None

    def update(self, id: int, data: Dict[str, Any]) -> bool:
        with DatabaseConnection(self.db_path) as cursor:
            cursor.execute("""
                UPDATE Truck_tank
                SET truck_tank_name = ?, pressure_type = ?, volume = ?,
                    degree_filling = ?, pressure = ?, temperature = ?,
                    component_enterprise = ?, spill_square = ?,
                    sub_id = ?, coordinate = ?
                WHERE truck_tank_id = ?
            """, (
                data['truck_tank_name'], data['pressure_type'], data['volume'],
                data['degree_filling'], data['pressure'], data['temperature'],
                data['component_enterprise'], data['spill_square'],
                data['sub_id'], data['coordinate'], id
            ))
            return cursor.rowcount > 0

    def delete(self, id: int) -> bool:
        with DatabaseConnection(self.db_path) as cursor:
            cursor.execute("DELETE FROM Truck_tank WHERE truck_tank_id = ?", (id,))
            return cursor.rowcount > 0

    def list_all(self) -> List[Dict[str, Any]]:
        with DatabaseConnection(self.db_path) as cursor:
            cursor.execute("SELECT * FROM Truck_tank")
            return [dict(row) for row in cursor.fetchall()]


# Пример использования:
if __name__ == "__main__":
    # Пример работы с технологическими устройствами
    device_crud = TechnologicalDeviceCRUD("db_eq.db")

    new_device_data = {
        "device_name": "Новый аппарат",
        "device_type": "Технологические аппараты",
        "volume": 200.0,
        "degree_filling": 0.7,
        "pressure": 2.5,
        "temperature": 35.0,
        "component_enterprise": "Установка 2",
        "spill_square": 75.0,
        "sub_id": 1,
        "coordinate": "55.123456, 37.123456"
    }

    # Create device
    new_device_id = device_crud.create(new_device_data)
    print(f"Created new device with ID: {new_device_id}")

    # Пример работы с автоцистернами
    truck_tank_crud = TruckTankCRUD("db_eq.db")

    new_truck_tank_data = {
        "truck_tank_name": "Новая автоцистерна",
        "pressure_type": "Под избыточным давлением",
        "volume": 30.0,
        "degree_filling": 0.85,
        "pressure": 1.8,
        "temperature": 20.0,
        "component_enterprise": "Площадка налива 1",
        "spill_square": 40.0,
        "sub_id": 1,
        "coordinate": "55.123456, 37.123456"
    }

    # Create truck tank
    new_truck_tank_id = truck_tank_crud.create(new_truck_tank_data)
    print(f"Created new truck tank with ID: {new_truck_tank_id}")