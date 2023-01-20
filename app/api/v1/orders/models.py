from sqlalchemy import Table, Column, Integer, String, Text, ForeignKey, PrimaryKeyConstraint, TIMESTAMP, Boolean

from app.db import db, metadata


orders = Table(
	"orders",
	metadata,
	Column("id", Integer, primary_key=True, index=True, autoincrement=True),
	Column("client_id", ForeignKey("clients.id"), nullable=False),
	Column("tz", Text, comment="Текст тз"),
	Column("start_ts", TIMESTAMP, nullable=False, comment="Дата создания заказа"),
	Column("deadline_ts", TIMESTAMP, nullable=False, comment="Дата дедлайна"),
	Column("end_ts", TIMESTAMP, comment="Дата завершения работы"),
	Column("comment", Text, comment="Комментарий к заказу"),
	Column("cost", Integer, nullable=False, comment="Стоимость работы"),
	Column("spent_hours", Integer, comment="Затраченное время"),
	Column("status", Integer, nullable=False, comment="Статус заказа")
)


order_files = Table(
	"order_files",
	metadata,
	Column("id", Integer, primary_key=True, index=True, autoincrement=True),
	Column("filepath", String(255), nullable=False, comment="Путь к файлу"),
	Column("upload_ts", TIMESTAMP, nullable=False, comment="Дата загрузки"),
	Column("is_result", Boolean, comment="Файл относится к результатам?")
)

order_changes_history = Table(
	"order_changes_history",
	metadata,
	Column("id", Integer, primary_key=True, index=True, autoincrement=True),
	Column("order_id", ForeignKey("orders.id"), index=True, comment="Id заказа"),
	Column("text", Text, comment="Текст изменения"),
	Column("create_ts", TIMESTAMP, nullable=False, comment="Дата создания изменения"),
	Column("status", Integer, nullable=False, comment="Статус заказа")
)


orders_order_files = Table(
	"orders_order_files",
	metadata,
	Column("id", Integer, primary_key=True, index=True, autoincrement=True),
	Column("order_id", ForeignKey("orders.id"), nullable=False, comment="Id заказа"),
	Column("change_id", ForeignKey("order_changes_history.id"), comment="Id изменения"),
	Column("order_file_id", ForeignKey("order_files.id"), comment="Id файла")
)
