import sqlite3
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from abc import ABC, abstractmethod


class DatabaseConnection:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        return self.conn.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.commit()
            self.conn.close()


class BaseEquipment(ABC):
    def __init__(self, db_path: str):
        self.db_path = db_path

    @abstractmethod
    def create(self, data: Dict[str, Any]) -> int:
        pass

    @abstractmethod
    def read(self, id: int) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def update(self, id: int, data: Dict[str, Any]) -> bool:
        pass

    @abstractmethod
    def delete(self, id: int) -> bool:
        pass

    @abstractmethod
    def list_all(self) -> List[Dict[str, Any]]:
        pass


@dataclass
class Tank:
    tank_id: Optional[int]
    tank_name: str
    tank_type: str
    volume: float
    degree_filling: float
    pressure: float
    temperature: float
    component_enterprise: str
    spill_square: float
    sub_id: int
    coordinate: str


class TankCRUD(BaseEquipment):
    def create(self, data: Dict[str, Any]) -> int:
        with DatabaseConnection(self.db_path) as cursor:
            cursor.execute("""
                INSERT INTO Tank (
                    tank_name, tank_type, volume, degree_filling,
                    pressure, temperature, component_enterprise,
                    spill_square, sub_id, coordinate
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data['tank_name'], data['tank_type'], data['volume'],
                data['degree_filling'], data['pressure'], data['temperature'],
                data['component_enterprise'], data['spill_square'],
                data['sub_id'], data['coordinate']
            ))
            return cursor.lastrowid

    def read(self, id: int) -> Optional[Dict[str, Any]]:
        with DatabaseConnection(self.db_path) as cursor:
            cursor.execute("""
                SELECT * FROM Tank WHERE tank_id = ?
            """, (id,))
            row = cursor.fetchone()
            if row:
                return dict(row)
            return None

    def update(self, id: int, data: Dict[str, Any]) -> bool:
        with DatabaseConnection(self.db_path) as cursor:
            cursor.execute("""
                UPDATE Tank
                SET tank_name = ?, tank_type = ?, volume = ?,
                    degree_filling = ?, pressure = ?, temperature = ?,
                    component_enterprise = ?, spill_square = ?,
                    sub_id = ?, coordinate = ?
                WHERE tank_id = ?
            """, (
                data['tank_name'], data['tank_type'], data['volume'],
                data['degree_filling'], data['pressure'], data['temperature'],
                data['component_enterprise'], data['spill_square'],
                data['sub_id'], data['coordinate'], id
            ))
            return cursor.rowcount > 0

    def delete(self, id: int) -> bool:
        with DatabaseConnection(self.db_path) as cursor:
            cursor.execute("DELETE FROM Tank WHERE tank_id = ?", (id,))
            return cursor.rowcount > 0

    def list_all(self) -> List[Dict[str, Any]]:
        with DatabaseConnection(self.db_path) as cursor:
            cursor.execute("SELECT * FROM Tank")
            return [dict(row) for row in cursor.fetchall()]


# Пример использования:
if __name__ == "__main__":
    tank_crud = TankCRUD("db_eq.db")

    # Создание нового танка
    new_tank_data = {
        "tank_name": "Новый резервуар",
        "tank_type": "Одностенный",
        "volume": 100.0,
        "degree_filling": 0.8,
        "pressure": 1.5,
        "temperature": 25.0,
        "component_enterprise": "Установка 1",
        "spill_square": 50.0,
        "sub_id": 1,
        "coordinate": "55.123456, 37.123456"
    }

    # Create
    new_id = tank_crud.create(new_tank_data)
    print(f"Created new tank with ID: {new_id}")

    # Read
    tank = tank_crud.read(new_id)
    print(f"Tank details: {tank}")

    # Update
    new_tank_data["tank_name"] = "Обновленный резервуар"
    success = tank_crud.update(new_id, new_tank_data)
    print(f"Update successful: {success}")

    # List all
    all_tanks = tank_crud.list_all()
    print(f"Total tanks: {len(all_tanks)}")

    # Delete
    deleted = tank_crud.delete(new_id)
    print(f"Delete successful: {deleted}")