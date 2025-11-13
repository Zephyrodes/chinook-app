from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from .database import Base

class Artist(Base):
    __tablename__ = "artist"
    ArtistId = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(120), nullable=False)
    albums = relationship("Album", back_populates="artist")

class Album(Base):
    __tablename__ = "album"
    AlbumId = Column(Integer, primary_key=True, autoincrement=True)
    Title = Column(String(160), nullable=False)
    ArtistId = Column(Integer, ForeignKey("artist.ArtistId"), nullable=False)
    artist = relationship("Artist", back_populates="albums")
    tracks = relationship("Track", back_populates="album")

class Genre(Base):
    __tablename__ = "genre"
    GenreId = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(120), nullable=False)
    tracks = relationship("Track", back_populates="genre")

class MediaType(Base):
    __tablename__ = "mediatype"
    MediaTypeId = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(120), nullable=False)
    tracks = relationship("Track", back_populates="mediatype")

class Track(Base):
    __tablename__ = "track"
    TrackId = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(200), nullable=False)
    AlbumId = Column(Integer, ForeignKey("album.AlbumId"), nullable=True)
    MediaTypeId = Column(Integer, ForeignKey("mediatype.MediaTypeId"), nullable=False)
    GenreId = Column(Integer, ForeignKey("genre.GenreId"), nullable=True)
    Composer = Column(String(220), nullable=True)
    Milliseconds = Column(Integer, nullable=False)
    Bytes = Column(Integer, nullable=True)
    UnitPrice = Column(Numeric(10, 2), nullable=False)
    album = relationship("Album", back_populates="tracks")
    mediatype = relationship("MediaType", back_populates="tracks")
    genre = relationship("Genre", back_populates="tracks")
    playlist_tracks = relationship("PlaylistTrack", back_populates="track")
    invoice_lines = relationship("InvoiceLine", back_populates="track")

class Playlist(Base):
    __tablename__ = "playlist"
    PlaylistId = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(120), nullable=False)
    playlist_tracks = relationship("PlaylistTrack", back_populates="playlist")

class PlaylistTrack(Base):
    __tablename__ = "playlisttrack"
    PlaylistId = Column(Integer, ForeignKey("playlist.PlaylistId"), primary_key=True)
    TrackId = Column(Integer, ForeignKey("track.TrackId"), primary_key=True)
    playlist = relationship("Playlist", back_populates="playlist_tracks")
    track = relationship("Track", back_populates="playlist_tracks")

class Employee(Base):
    __tablename__ = "employee"
    EmployeeId = Column(Integer, primary_key=True, autoincrement=True)
    LastName = Column(String(20), nullable=False)
    FirstName = Column(String(20), nullable=False)
    Title = Column(String(30), nullable=True)
    ReportsTo = Column(Integer, ForeignKey("employee.EmployeeId"), nullable=True)
    BirthDate = Column(DateTime, nullable=True)
    HireDate = Column(DateTime, nullable=True)
    Address = Column(String(70), nullable=True)
    City = Column(String(40), nullable=True)
    State = Column(String(40), nullable=True)
    Country = Column(String(40), nullable=True)
    PostalCode = Column(String(10), nullable=True)
    Phone = Column(String(24), nullable=True)
    Fax = Column(String(24), nullable=True)
    Email = Column(String(60), nullable=True)
    # Self-referential relationship
    manager = relationship("Employee", remote_side=[EmployeeId], back_populates="subordinates")
    subordinates = relationship("Employee", back_populates="manager")
    customers = relationship("Customer", back_populates="support_rep")

class Customer(Base):
    __tablename__ = "customer"
    CustomerId = Column(Integer, primary_key=True, autoincrement=True)
    FirstName = Column(String(40), nullable=False)
    LastName = Column(String(20), nullable=False)
    Company = Column(String(80), nullable=True)
    Address = Column(String(70), nullable=True)
    City = Column(String(40), nullable=True)
    State = Column(String(40), nullable=True)
    Country = Column(String(40), nullable=True)
    PostalCode = Column(String(10), nullable=True)
    Phone = Column(String(24), nullable=True)
    Fax = Column(String(24), nullable=True)
    Email = Column(String(60), nullable=False)
    SupportRepId = Column(Integer, ForeignKey("employee.EmployeeId"), nullable=True)
    support_rep = relationship("Employee", back_populates="customers")
    invoices = relationship("Invoice", back_populates="customer")

class Invoice(Base):
    __tablename__ = "invoice"
    InvoiceId = Column(Integer, primary_key=True, autoincrement=True)
    CustomerId = Column(Integer, ForeignKey("customer.CustomerId"), nullable=False)
    InvoiceDate = Column(DateTime, nullable=False)
    BillingAddress = Column(String(70), nullable=True)
    BillingCity = Column(String(40), nullable=True)
    BillingState = Column(String(40), nullable=True)
    BillingCountry = Column(String(40), nullable=True)
    BillingPostalCode = Column(String(10), nullable=True)
    Total = Column(Numeric(10, 2), nullable=False)
    customer = relationship("Customer", back_populates="invoices")
    lines = relationship("InvoiceLine", back_populates="invoice", cascade="all, delete-orphan")

class InvoiceLine(Base):
    __tablename__ = "invoiceline"
    InvoiceLineId = Column(Integer, primary_key=True, autoincrement=True)
    InvoiceId = Column(Integer, ForeignKey("invoice.InvoiceId"), nullable=False)
    TrackId = Column(Integer, ForeignKey("track.TrackId"), nullable=False)
    UnitPrice = Column(Numeric(10, 2), nullable=False)
    Quantity = Column(Integer, nullable=False)
    invoice = relationship("Invoice", back_populates="lines")
    track = relationship("Track", back_populates="invoice_lines")