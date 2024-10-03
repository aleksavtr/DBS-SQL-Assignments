DROP SCHEMA IF EXISTS schema CASCADE ;
CREATE SCHEMA IF NOT EXISTS schema;

CREATE TYPE schema.status_item AS ENUM ('in_stock', 'available', 'on_quality_check', 'on_the_way','on_the_exhibition','loaned','not qualitative');
CREATE TYPE schema.name_category AS ENUM ('Paintings', 'Sculptures', ' Photography', 'Textiles','Ceramics and Pottery','Digital Art');
CREATE TYPE schema.status_exhibition AS ENUM ('Planned', 'Active', ' Closed', 'Cancelled');
CREATE TYPE schema.status_zone AS ENUM('reserved','active');
CREATE TABLE schema.Zone (
    ID SERIAL PRIMARY KEY,
    Name VARCHAR(100) NOT NULL UNIQUE,
    Capacity INT NOT NULL CHECK (Capacity >= 0)
);
CREATE TABLE schema.Item (
    ID SERIAL PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Status schema.status_item NOT NULL,
    Owner VARCHAR(50) NOT NULL,
    Qual_check BOOLEAN NOT NULL DEFAULT FALSE,
    ZoneID INT ,
    FOREIGN KEY (ZoneID)  REFERENCES schema.Zone(ID)
);

CREATE TABLE schema.Category (
    ID SERIAL PRIMARY KEY,
    Name schema.name_category NOT NULL ,
    Description TEXT,
    Item_ID INT NOT NULL,
    FOREIGN KEY (Item_ID) REFERENCES schema.Item(ID)
);

CREATE TABLE schema.Exhibition (
    ID SERIAL PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    StartDate TIMESTAMP NOT NULL,
    EndDate TIMESTAMP NOT NULL,
    Status schema.status_exhibition NOT NULL
);

CREATE TABLE schema.Loans (
    ID SERIAL PRIMARY KEY,
    Item_id INT NOT NULL,
    DateLoan TIMESTAMP NOT NULL,
    ReturnDate TIMESTAMP NOT NULL,
    Real_ret_date TIMESTAMP,
    Borrower VARCHAR(100) NOT NULL,
    Is_permanent BOOLEAN NOT NULL DEFAULT FALSE,
    FOREIGN KEY (Item_id) REFERENCES schema.Item(ID)
);

CREATE TABLE schema.QualityCheck (
    ID SERIAL PRIMARY KEY,
    Item_id INT NOT NULL,
    DateSent TIMESTAMP NOT NULL,
    ReturnDate TIMESTAMP NOT NULL,
    StartDate TIMESTAMP NOT NULL,
    EndDate TIMESTAMP NOT NULL,
    ResultState BOOLEAN NOT NULL,
    FOREIGN KEY (Item_id) REFERENCES schema.Item(ID)
);


CREATE TABLE schema.ExhibitionHistory (
    ID SERIAL PRIMARY KEY,
    Exhibition_id INT NOT NULL,
    StartDate TIMESTAMP NOT NULL,
    EndDate TIMESTAMP NOT NULL,
    Overview TEXT,
    Is_recurring BOOLEAN NOT NULL,
    FOREIGN KEY (Exhibition_id) REFERENCES schema.Exhibition(ID)
);

CREATE TABLE schema.ExhibitionZone (
    ID_Zone INT NOT NULL,
    ID_Exh INT NOT NULL,
    Status schema.status_zone NOT NULL,
    FOREIGN KEY (ID_Zone) REFERENCES schema.Zone(ID),
    FOREIGN KEY (ID_Exh) REFERENCES schema.Exhibition(ID)
);

CREATE TABLE schema.Exhibition_Item (
    Item_id INT NOT NULL,
    Exhibition_Id INT NOT NULL,
    Status schema.status_exhibition NOT NULL,
    FOREIGN KEY (Item_id) REFERENCES schema.Item(ID),
    FOREIGN KEY (Exhibition_Id) REFERENCES schema.Exhibition(ID)
);