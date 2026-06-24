-- Initial SQL migration for eezy_source models
-- Generated from: eezy_source/models.py
-- Dialect: MySQL 8+

SET NAMES utf8mb4;
SET time_zone = '+00:00';

CREATE TABLE IF NOT EXISTS eezy_source_processconfig (
    processConfigId INT AUTO_INCREMENT PRIMARY KEY,
    processCode VARCHAR(100) NOT NULL,
    sellerShipperDeliveryFee DOUBLE NULL,
    sellerShipperDeliveryFeeUnit VARCHAR(100) NULL,
    handlingFee DOUBLE NULL,
    handlingFeeUnit VARCHAR(100) NULL,
    weightUnit VARCHAR(100) NULL,
    shippingMode VARCHAR(100) NULL,
    customRate DOUBLE NULL,
    customRateUnit VARCHAR(100) NULL,
    shippingMargin DOUBLE NULL,
    shippingMarginUnit VARCHAR(100) NULL,
    defaultCurrency VARCHAR(100) NULL,
    active TINYINT(1) NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS eezy_source_receipt (
    receiptId INT AUTO_INCREMENT PRIMARY KEY,
    receiptCode VARCHAR(100) NOT NULL,
    receiptName VARCHAR(100) NULL,
    active TINYINT(1) NOT NULL DEFAULT 1,
    created_by VARCHAR(100) NULL,
    updated_by VARCHAR(100) NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS eezy_source_record (
    recordId INT AUTO_INCREMENT PRIMARY KEY,
    itemName VARCHAR(40) NOT NULL,
    itemCost DOUBLE NULL,
    quantity INT NULL,
    totalCost DOUBLE NULL,
    receipt_id INT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    active SMALLINT NULL,
    CONSTRAINT fk_record_receipt
        FOREIGN KEY (receipt_id)
        REFERENCES eezy_source_receipt(receiptId)
        ON DELETE CASCADE,
    INDEX idx_record_receipt_id (receipt_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS eezy_source_systemunits (
    systemUnitId INT AUTO_INCREMENT PRIMARY KEY,
    unitName VARCHAR(100) NULL,
    unitCode VARCHAR(100) NULL,
    unitSymbol VARCHAR(100) NULL,
    unitDescription LONGTEXT NULL,
    unitType VARCHAR(100) NULL,
    active TINYINT(1) NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS eezy_source_currency (
    currencyId INT AUTO_INCREMENT PRIMARY KEY,
    currencyName VARCHAR(100) NULL,
    currencyCode VARCHAR(100) NULL,
    currencySymbol VARCHAR(100) NULL,
    active TINYINT(1) NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS eezy_source_fx (
    fxId INT AUTO_INCREMENT PRIMARY KEY,
    sendCurrency_id INT NOT NULL,
    receiveCurrency_id INT NOT NULL,
    exchangeRate DOUBLE NULL,
    active TINYINT(1) NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_fx_send_currency
        FOREIGN KEY (sendCurrency_id)
        REFERENCES eezy_source_currency(currencyId)
        ON DELETE CASCADE,
    CONSTRAINT fk_fx_receive_currency
        FOREIGN KEY (receiveCurrency_id)
        REFERENCES eezy_source_currency(currencyId)
        ON DELETE CASCADE,
    INDEX idx_fx_send_currency_id (sendCurrency_id),
    INDEX idx_fx_receive_currency_id (receiveCurrency_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
