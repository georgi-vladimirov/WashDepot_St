from datetime import date
from decimal import Decimal
from typing import ClassVar

from sqlalchemy import (
    Column,
    ForeignKey,
    Numeric,
    String,
    Table,
    Text,
    UniqueConstraint,
    inspect,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from core.db import Base
from core.models.base import BaseModel

# --- Association tables (many-to-many) ---

service_price_locations = Table(
    "core_service_price_locations",
    Base.metadata,
    Column(
        "service_price_id",
        ForeignKey("core_service_prices.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "location_id",
        ForeignKey("core_locations.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)

subscriber_locations = Table(
    "core_subscriber_locations",
    Base.metadata,
    Column(
        "subscriber_id",
        ForeignKey("core_subscribers.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "location_id",
        ForeignKey("core_locations.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Location(BaseModel):
    __tablename__ = "core_locations"

    name: Mapped[str] = mapped_column(String(100), unique=True)
    short_name: Mapped[str] = mapped_column(String(4), unique=True)

    service_prices: Mapped[list["ServicePrice"]] = relationship(
        secondary=service_price_locations, back_populates="locations"
    )
    subscribers: Mapped[list["Subscriber"]] = relationship(
        secondary=subscriber_locations, back_populates="locations"
    )
    employees: Mapped[list["Employee"]] = relationship(back_populates="location")

    def __str__(self) -> str:
        return f"{self.name} - {self.short_name}"


class VehicleType(BaseModel):
    __tablename__ = "core_vehicle_types"

    name: Mapped[str] = mapped_column(String(20), unique=True)

    def __str__(self) -> str:
        return self.name


class ServiceType(BaseModel):
    __tablename__ = "core_service_types"

    name: Mapped[str] = mapped_column(String(50), unique=True)
    name_bg: Mapped[str] = mapped_column(String(100), unique=True, default="")
    selectivity: Mapped[int] = mapped_column(default=1)
    order: Mapped[int] = mapped_column(default=1)

    services: Mapped[list["Service"]] = relationship(back_populates="service_type")

    def __str__(self) -> str:
        return self.name


class Service(BaseModel):
    __tablename__ = "core_services"

    name: Mapped[str] = mapped_column(String(200), unique=True)
    service_type_id: Mapped[int] = mapped_column(
        ForeignKey("core_service_types.id", ondelete="CASCADE")
    )
    description: Mapped[str] = mapped_column(Text, default="")

    service_type: Mapped["ServiceType"] = relationship(
        back_populates="services"
    )
    service_prices: Mapped[list["ServicePrice"]] = relationship(
        back_populates="service"
    )

    def __str__(self) -> str:
        return f"{self.name}"


class ServicePrice(BaseModel):
    __tablename__ = "core_service_prices"

    vehicle_type_id: Mapped[int] = mapped_column(
        ForeignKey("core_vehicle_types.id", ondelete="CASCADE")
    )
    service_id: Mapped[int] = mapped_column(
        ForeignKey("core_services.id", ondelete="CASCADE")
    )
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))

    vehicle_type: Mapped["VehicleType"] = relationship()
    service: Mapped["Service"] = relationship(back_populates="service_prices")
    locations: Mapped[list["Location"]] = relationship(
        secondary=service_price_locations, back_populates="service_prices"
    )
    IMMUTABLE_FIELDS: ClassVar[set[str]] = {"vehicle_type_id", "service_id", "amount"}

    @validates("vehicle_type_id", "service_id", "amount")
    def _validate_immutable(self, key: str, value):
        if inspect(self).persistent and getattr(self, key) != value:
            raise ValueError(
                f"ServicePrice field '{key}' cannot be modified after creation."
            )
        return value

    def soft_delete(self) -> None:
        """Вместо изтриване — деактивиране (ценовата история се пази)."""
        self.is_active = False

    def __str__(self) -> str:
        locations = ", ".join(loc.name for loc in self.locations)
        return f"{self.service.name} - {self.vehicle_type.name} @ {locations}: {self.amount}"


class VehicleBrand(BaseModel):
    __tablename__ = "core_vehicle_brands"

    brand: Mapped[str] = mapped_column(String(50), unique=True)
    number_sort: Mapped[int]

    def __str__(self) -> str:
        return f"{self.brand}"


class EmployeePosition(BaseModel):
    __tablename__ = "core_employee_positions"

    position: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[str] = mapped_column(Text, default="")

    employees: Mapped[list["Employee"]] = relationship(back_populates="position")

    def __str__(self) -> str:
        return f"{self.position} | Active: {self.is_active}"


class Employee(BaseModel):
    __tablename__ = "core_employees"

    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    employee_id: Mapped[str] = mapped_column(String(50), unique=True)
    position_id: Mapped[int] = mapped_column(
        ForeignKey("core_employee_positions.id", ondelete="CASCADE")
    )
    location_id: Mapped[int] = mapped_column(
        ForeignKey("core_locations.id", ondelete="CASCADE")
    )
    salary_percentage: Mapped[Decimal] = mapped_column(
        Numeric(5, 2), default=Decimal(0)
    )
    bonus_percentage: Mapped[Decimal] = mapped_column(
        Numeric(5, 2), default=Decimal(0)
    )

    position: Mapped["EmployeePosition"] = relationship(back_populates="employees")
    location: Mapped["Location"] = relationship(back_populates="employees")

    def __str__(self) -> str:
        return f"{self.employee_id} ({self.first_name} {self.last_name})"


class Subscriber(BaseModel):
    __tablename__ = "core_subscribers"

    name: Mapped[str] = mapped_column(String(100), unique=True)
    company_id: Mapped[str] = mapped_column(String(10), unique=True)
    discount_percentage: Mapped[Decimal] = mapped_column(
        Numeric(5, 2), default=Decimal(0)
    )

    locations: Mapped[list["Location"]] = relationship(
        secondary=subscriber_locations, back_populates="subscribers"
    )

    def __str__(self) -> str:
        return f"{self.name}"


class CalendarEvent(BaseModel):
    __tablename__ = "core_calendar_events"
    __table_args__ = (UniqueConstraint("date", "location_id"),)

    date: Mapped[date]
    location_id: Mapped[int] = mapped_column(
        ForeignKey("core_locations.id", ondelete="CASCADE")
    )

    location: Mapped["Location"] = relationship()

    def __str__(self) -> str:
        return f"{self.date} - {self.location.name}"
