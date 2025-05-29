CREATE OR REPLACE PROCEDURE silver.load_silver()
LANGUAGE plpgsql
AS $$
DECLARE
	start_time TIMESTAMP;
	end_time TIMESTAMP;
	silver_time TIMESTAMP;
	silver_end_time TIMESTAMP;
BEGIN
	silver_time := NOW();
	-- Load crm_cust_info
	start_time := NOW();
	RAISE NOTICE '================================================';
    RAISE NOTICE 'Loading Silver Layer';
    RAISE NOTICE '================================================';

	RAISE NOTICE '================================================';
	RAISE NOTICE 'Loading CRM Tables';
	RAISE NOTICE '================================================';
	TRUNCATE TABLE silver.crm_cust_info;
	INSERT INTO silver.crm_cust_info (
		cst_id,
		cst_key,
		cst_firstname,
		cst_lastname,
		cst_material_status,
		cst_gndr,
		cst_create_date)
	SELECT
		cst_id,
		cst_key,
		TRIM(cst_firstname),
		TRIM(cst_lastname),
		CASE 
			WHEN UPPER(TRIM(cst_material_status)) = 'S' THEN 'Single'
			WHEN UPPER(TRIM(cst_material_status)) = 'M' THEN 'Married'
			ELSE 'n/a'
		END,
		CASE 
			WHEN UPPER(TRIM(cst_gndr)) = 'F' THEN 'Female'
			WHEN UPPER(TRIM(cst_gndr)) = 'M' THEN 'Male'
			ELSE 'n/a'
		END,
		cst_create_date
	FROM (
		SELECT *, ROW_NUMBER() OVER (PARTITION BY cst_id ORDER BY cst_create_date DESC) as flag_last
		FROM bronze.crm_cust_info
		WHERE cst_id IS NOT NULL
	) t 
	WHERE flag_last = 1;

	end_time := NOW();
	RAISE NOTICE 'Load crm_cust_info duration: % seconds', EXTRACT(EPOCH FROM end_time - start_time);

	-- Load crm_prd_info
	start_time := NOW();
	TRUNCATE TABLE silver.crm_prd_info;
	INSERT INTO silver.crm_prd_info (
		prd_id,
		cat_id,
		prd_key,
		prd_nm,
		prd_cost,
		prd_line,
		prd_start_dt,
		prd_end_dt
	)
	SELECT
		prd_id,
		REPLACE(SUBSTRING(prd_key, 1, 5), '-', '_'),
		SUBSTRING(prd_key, 7, LENGTH(prd_key)),
		prd_nm,
		COALESCE(prd_cost, 0),
		CASE 
			WHEN UPPER(TRIM(prd_line)) = 'M' THEN 'Mountain'
			WHEN UPPER(TRIM(prd_line)) = 'R' THEN 'Road'
			WHEN UPPER(TRIM(prd_line)) = 'S' THEN 'Other Sales'
			WHEN UPPER(TRIM(prd_line)) = 'T' THEN 'Touring'
			ELSE 'n/a'
		END,
		CAST(prd_start_dt AS DATE),
		CAST(LEAD(prd_start_dt) OVER (PARTITION BY prd_key ORDER BY prd_start_dt) - INTERVAL '1 day' AS DATE)
	FROM bronze.crm_prd_info;

	end_time := NOW();
	RAISE NOTICE 'Load crm_prd_info duration: % seconds', EXTRACT(EPOCH FROM end_time - start_time);

	-- Load crm_sales_details
	start_time := NOW();
	TRUNCATE TABLE silver.crm_sales_details;
	INSERT INTO silver.crm_sales_details (
		sls_ord_num,
		sls_prd_key,
		sls_cust_id,
		sls_order_dt,
		sls_ship_dt,
		sls_due_dt,
		sls_sales,
		sls_quantity,
		sls_price
	)
	SELECT 
		sls_ord_num,
		sls_prd_key,
		sls_cust_id,
		CASE WHEN sls_order_dt = 0 OR LENGTH(sls_order_dt::text) != 8 THEN NULL
			 ELSE TO_DATE(sls_order_dt::text, 'YYYYMMDD')
		END,
		CASE WHEN sls_ship_dt = 0 OR LENGTH(sls_ship_dt::text) != 8 THEN NULL
			 ELSE TO_DATE(sls_ship_dt::text, 'YYYYMMDD')
		END,
		CASE WHEN sls_due_dt = 0 OR LENGTH(sls_due_dt::text) != 8 THEN NULL
			 ELSE TO_DATE(sls_due_dt::text, 'YYYYMMDD')
		END,
		CASE WHEN sls_sales IS NULL OR sls_sales <= 0 OR sls_sales != sls_quantity * ABS(sls_price)
			 THEN sls_quantity * ABS(sls_price)
			 ELSE sls_sales
		END,
		sls_quantity,
		CASE WHEN sls_price IS NULL OR sls_price <= 0
			 THEN sls_sales / NULLIF(sls_quantity, 0)
			 ELSE sls_price
		END
	FROM bronze.crm_sales_details;

	end_time := NOW();
	RAISE NOTICE 'Load crm_sales_details duration: % seconds', EXTRACT(EPOCH FROM end_time - start_time);
	RAISE NOTICE '================================================';
	RAISE NOTICE 'Loading ERP Tables';
	RAISE NOTICE '================================================';
	-- Load erp_cust_az12
	start_time := NOW();

	TRUNCATE TABLE silver.erp_cust_az12;
	INSERT INTO silver.erp_cust_az12 (
		cid,
		bdate,
		gen
	)
	SELECT
		CASE WHEN cid LIKE 'NAS%' THEN SUBSTRING(cid::text, 4, LENGTH(cid::text))
			 ELSE cid::text
		END,
		CASE WHEN bdate > CURRENT_DATE THEN NULL ELSE bdate END,
		CASE 
			WHEN UPPER(TRIM(gen)) IN ('F', 'FEMALE') THEN 'Female'
			WHEN UPPER(TRIM(gen)) IN ('M', 'MALE') THEN 'Male'
			ELSE 'n/a'
		END
	FROM bronze.erp_cust_az12;

	end_time := NOW();
	RAISE NOTICE 'Load erp_cust_az12 duration: % seconds', EXTRACT(EPOCH FROM end_time - start_time);

	-- Load erp_loc_a101
	start_time := NOW();
	TRUNCATE TABLE silver.erp_loc_a101;
	INSERT INTO silver.erp_loc_a101 (
		cid,
		cntry
	)
	SELECT
		REPLACE(cid, '-', ''),
		CASE
			WHEN TRIM(cntry) = 'DE' THEN 'Germany'
			WHEN TRIM(cntry) IN ('US', 'USA') THEN 'United States'
			WHEN TRIM(cntry) = '' OR cntry IS NULL THEN 'n/a'
			ELSE TRIM(cntry)
		END
	FROM bronze.erp_loc_a101;

	end_time := NOW();
	RAISE NOTICE 'Load erp_loc_a101 duration: % seconds', EXTRACT(EPOCH FROM end_time - start_time);

	-- Load erp_px_cat_g1v2
	start_time := NOW();
	TRUNCATE TABLE silver.erp_px_cat_g1v2;
	INSERT INTO silver.erp_px_cat_g1v2 (
		id,
		cat,
		subcat,
		maintenance
	)
	SELECT
		id,
		cat,
		subcat,
		maintenance
	FROM bronze.erp_px_cat_g1v2;

	end_time := NOW();
	RAISE NOTICE 'Load erp_px_cat_g1v2 duration: % seconds', EXTRACT(EPOCH FROM end_time - start_time);

	silver_end_time := NOW();
	RAISE NOTICE '==========================================';
    RAISE NOTICE 'Total Load Duration: % seconds', EXTRACT(EPOCH FROM silver_end_time - silver_time);
	RAISE NOTICE '==========================================';
EXCEPTION
	WHEN OTHERS THEN
		RAISE NOTICE '==========================================';
		RAISE NOTICE 'ERROR OCCURRED DURING LOADING SILVER LAYER';
		RAISE NOTICE 'Error: %', SQLERRM;
		RAISE NOTICE '==========================================';
END;
$$;

CALL silver.load_silver();
