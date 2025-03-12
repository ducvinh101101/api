import json
from flask import request, jsonify
from sqlalchemy import create_engine, text
from decimal import Decimal
class user_model():
    def __init__(self):
        try:
            server = 'DESKTOP-PIULBJ0\SQLEXPRESS'
            database = 'BT1'
            driver = 'ODBC Driver 17 for SQL Server'
            conn_str = f'mssql+pyodbc://@{server}/{database}?trusted_connection=yes&driver={driver}'
            self.engine = create_engine(conn_str)
            self.engine.autocommit = True
            print('✅ Connected to database successfully!')
        except Exception as e:
            print(f'❌ Connection failed: {e}')

    def user_login(self):
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("SELECT TOP 5 * FROM tSach"))
                rows = [dict(zip(result.keys(), self.convert_decimal(row))) for row in result]
                return json.dumps(rows, indent=4, ensure_ascii=False)
        except Exception as e:
            return f"❌ Query failed: {e}"

    def convert_decimal(self, row):
        """Chuyển đổi tất cả các giá trị Decimal trong row thành float"""
        return [float(x) if isinstance(x, Decimal) else x for x in row]

    def user_signin(self,data):
        try:
            with self.engine.connect() as conn:
                data = request.get_json()
                sql = text("""
                                    INSERT INTO tSach 
                                    (MaSach, TenSach, TacGia, MaTheLoai, MaNXB, DonGiaNhap, DonGiaBan, SoLuong, SoTrang, TrongLuong, Anh, TrangThai) 
                                    VALUES 
                                    (:MaSach, :TenSach, :TacGia, :MaTheLoai, :MaNXB, :DonGiaNhap, :DonGiaBan, :SoLuong, :SoTrang, :TrongLuong, :Anh, :TrangThai)
                                """)
                conn.execute(sql, data)
                conn.commit()
                return "✅ Insert thành công!"
        except Exception as e:
            return f"❌ Query failed: {e}"

    def user_update(self,data):
        try:
            data = request.get_json()
            if "MaSach" not in data:
                return jsonify({"error": "❌ Thiếu 'MaSach' để cập nhật!"}), 400
            if "TrangThai" in data:
                if data["TrangThai"] == "Còn hàng":
                    data["TrangThai"] = 1
                elif data["TrangThai"] == "Hết hàng":
                    data["TrangThai"] = 0
                elif data["TrangThai"] is not None:
                    return jsonify({"error": "❌ Giá trị 'TrangThai' không hợp lệ!"}), 400
            check_sql = text("SELECT COUNT(*) FROM tSach WHERE MaSach = :MaSach")
            with self.engine.connect() as conn:
                result = conn.execute(check_sql, {"MaSach": data["MaSach"]}).scalar()
                if result == 0:
                    return jsonify({"error": "❌ Sách không tồn tại!"}), 404
            sql = text("""
                        UPDATE tSach 
                        SET TenSach = :TenSach, TacGia = :TacGia, MaTheLoai = :MaTheLoai, 
                            MaNXB = :MaNXB, DonGiaNhap = :DonGiaNhap, DonGiaBan = :DonGiaBan, 
                            SoLuong = :SoLuong, SoTrang = :SoTrang, TrongLuong = :TrongLuong, 
                            Anh = :Anh, TrangThai = :TrangThai
                        WHERE MaSach = :MaSach
                    """)
            with self.engine.connect() as conn:
                conn.execute(sql, data)
                conn.commit()
            return jsonify({"message": "✅ Update thành công!"}), 200
        except Exception as e:
            return f"❌ Query failed: {e}"
    def user_delete(self, id):
        try:
            sql_check = text("SELECT COUNT(*) FROM tSach WHERE MaSach = :id")
            sql_delete = text("DELETE FROM tSach WHERE MaSach = :id")
            with self.engine.connect() as conn:
                result = conn.execute(sql_check, {"id": str(id)}).scalar()
                if result == 0:
                    return jsonify({"error": "❌ Sách không tồn tại!"}), 404
            with self.engine.begin() as conn:
                conn.execute(sql_delete, {"id": str(id)})

            return jsonify({"message": "✅ Xóa sách thành công!"}), 200
        except Exception as e:
            return jsonify({"error": f"❌ Query failed: {str(e)}"}), 400



