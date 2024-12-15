from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from db_CRUD_tank import BaseEquipment, DatabaseConnection  # Импортируем из первого файла


@dataclass
class Compressor:
    comp_id: Optional[int]
    comp_name: str
    comp_type: str
    volume: float
    flow: float
    time_out: float
    pressure: float
    temperature: float
    component_enterprise: str
    sub_id: int
    coordinate: str


class CompressorCRUD(BaseEquipment):
    def create(self, data: Dict[str, Any]) -> int:
        with DatabaseConnection(self.db_path) as cursor:
            cursor.execute("""
                INSERT INTO Compressor (
                    comp_name, comp_type, volume, flow, time_out,
                    pressure, temperature, component_enterprise,
                    sub_id, coordinate
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data['comp_name'], data['comp_type'], data['volume'],
                data['flow'], data['time_out'], data['pressure'],
                data['temperature'], data['component_enterprise'],
                data['sub_id'], data['coordinate']
            ))
            return cursor.lastrowid

    def read(self, id: int) -> Optional[Dict[str, Any]]:
        with DatabaseConnection(self.db_path) as cursor:
            cursor.execute("SELECT * FROM Compressor WHERE comp_id = ?", (id,))
            row = cursor.fetchone()
            if row:
                return dict(row)
            return None

    def update(self, id: int, data: Dict[str, Any]) -> bool:
        with DatabaseConnection(self.db_path) as cursor:
            cursor.execute("""
                UPDATE Compressor
                SET comp_name = ?, comp_type = ?, volume = ?,
                    flow = ?, time_out = ?, pressure = ?,
                    temperature = ?, component_enterprise = ?,
                    sub_id = ?, coordinate = ?
                WHERE comp_id = ?
            """, (
                data['comp_name'], data['comp_type'], data['volume'],
                data['flow'], data['time_out'], data['pressure'],
                data['temperature'], data['component_enterprise'],
                data['sub_id'], data['coordinate'], id
            ))
            return cursor.rowcount > 0

    def delete(self, id: int) -> bool:
        with DatabaseConnection(self.db_path) as cursor:
            cursor.execute("DELETE FROM Compressor WHERE comp_id = ?", (id,))
            return cursor.rowcount > 0

    def list_all(self) -> List[Dict[str, Any]]:
        with DatabaseConnection(self.db_path) as cursor:
            cursor.execute("SELECT * FROM Compressor")
            return [dict(row) for row in cursor.fetchall()]


# Пример использования:
if __name__ == "__main__":
    compressor_crud = CompressorCRUD("db_eq.db")

    new_compressor_data = {
        "comp_name": "Новый компрессор",
        "comp_type": "Центробежный",
        "volume": 150.0,
        "flow": 200.0,
        "time_out": 1.5,
        "pressure": 4.0,
        "temperature": 40.0,
        "component_enterprise": "Компрессорная станция 1",
        "sub_id": 1,
        "coordinate": "55.123456, 37.123456"
    }

    # Create
    new_comp_id = compressor_crud.create(new_compressor_data)
    print(f"Created new compressor with ID: {new_comp_id}")

    # Read
    compressor = compressor_crud.read(new_comp_id)
    print(f"Compressor details: {compressor}")

    # Update
    new_compressor_data["comp_name"] = "Обновленный компрессор"
    success = compressor_crud.update(new_comp_id, new_compressor_data)
    print(f"Update successful: {success}")

    # List all
    all_compressors = compressor_crud.list_all()
    print(f"Total compressors: {len(all_compressors)}")

    # Delete
    deleted = compressor_crud.delete(new_comp_id)
    print(f"Delete successful: {deleted}")