CREATE OR REPLACE PROCEDURE bronze.load_bronze()
LANGUAGE plpgsql
AS $$
DECLARE 
	start_time TIMESTAMP;
	end_time TIMESTAMP;
	bronze_start_time TIMESTAMP;
	bronze_end_time TIMESTAMP;
BEGIN
		bronze_start_time := NOW();
		RAISE NOTICE '======================================';
		RAISE NOTICE 'Loading Bronze Layer';
		RAISE NOTICE '======================================';
	
		RAISE NOTICE '======================================';
		RAISE NOTICE 'Loading Crm Tables';
		RAISE NOTICE '======================================';
		start_time := NOW();
		RAISE NOTICE '>> Truncating Table: bronze.crm_cust_info';
		TRUNCATE TABLE bronze.crm_cust_info;
		RAISE NOTICE '>> Inserting Data Into: bronze.crm_cust_info';
		COPY bronze.crm_cust_info 
		FROM 'C:/sql-data-warehouse-project/sql-data-warehouse-project/datasets/source_crm/cust_info.csv' 
		WITH (
			FORMAT csv,
			HEADER true,
			DELIMITER ','
		);
		end_time := NOW();
		RAISE NOTICE 'Load duration: % segundos', EXTRACT(EPOCH FROM end_time - start_time);

		start_time := NOW();
		RAISE NOTICE '>> Truncating Table: bronze.crm_prd_info';
		TRUNCATE TABLE bronze.crm_prd_info;
		RAISE NOTICE '>> Inserting Data Into: bronze.crm_prd_info';
		COPY bronze.crm_prd_info 
		FROM 'C:/sql-data-warehouse-project/sql-data-warehouse-project/datasets/source_crm/prd_info.csv' 
		WITH (
			FORMAT csv,
			HEADER true,
			DELIMITER ','
		);
		end_time := NOW();
		RAISE NOTICE 'Load duration: % segundos', EXTRACT(EPOCH FROM end_time - start_time);


		start_time := NOW();
		RAISE NOTICE '>> Truncating Table: bronze.crm_sales_details';
		TRUNCATE TABLE bronze.crm_sales_details;
		RAISE NOTICE '>> Inserting Data Into: bronze.crm_sales_details';
		COPY bronze.crm_sales_details
		FROM 'C:/sql-data-warehouse-project/sql-data-warehouse-project/datasets/source_crm/sales_details.csv' 
		WITH (
			FORMAT csv,
			HEADER true,
			DELIMITER ','
		);		
		end_time := NOW();
		RAISE NOTICE 'Load duration: % segundos', EXTRACT(EPOCH FROM end_time - start_time);

		
		RAISE NOTICE '======================================';
		RAISE NOTICE 'Loading Erp Tables';
		RAISE NOTICE '======================================';

		start_time := NOW();
		RAISE NOTICE '>> Truncating Table: bronze.erp_cust_az12';
		TRUNCATE TABLE bronze.erp_cust_az12;
		RAISE NOTICE '>> Inserting Data Into: bronze.erp_cust_az12';
		COPY bronze.erp_cust_az12
		FROM 'C:/sql-data-warehouse-project/sql-data-warehouse-project/datasets/source_erp/cust_az12.csv' 
		WITH (
			FORMAT csv,
			HEADER true,
			DELIMITER ','
		);		
		end_time := NOW();
		RAISE NOTICE 'Load duration: % segundos', EXTRACT(EPOCH FROM end_time - start_time);


		start_time := NOW();
		RAISE NOTICE '>> Truncating Table: bronze.erp_loc_a101';
		TRUNCATE TABLE bronze.erp_loc_a101;
		RAISE NOTICE '>> Inserting Data Into: bronze.erp_loc_a101';
		COPY bronze.erp_loc_a101
		FROM 'C:/sql-data-warehouse-project/sql-data-warehouse-project/datasets/source_erp/loc_a101.csv' 
		WITH (
			FORMAT csv,
			HEADER true,
			DELIMITER ','
		);		
		end_time := NOW();
		RAISE NOTICE 'Load duration: % segundos', EXTRACT(EPOCH FROM end_time - start_time);


		start_time := NOW();
		RAISE NOTICE '>> Truncating Table: bronze.erp_px_cat_g1v2';
		TRUNCATE TABLE bronze.erp_px_cat_g1v2;
		RAISE NOTICE '>> Inserting Data Into: bronze.erp_px_cat_g1v2';
		COPY bronze.erp_px_cat_g1v2
		FROM 'C:/sql-data-warehouse-project/sql-data-warehouse-project/datasets/source_erp/px_cat_g1v2.csv' 
		WITH (
			FORMAT csv,
			HEADER true,
			DELIMITER ','
		);
		end_time := NOW();
		RAISE NOTICE 'Load duration: % segundos', EXTRACT(EPOCH FROM end_time - start_time);

		bronze_end_time := NOW();
		RAISE NOTICE 'Load Bronze duration: % segundos', EXTRACT(EPOCH FROM bronze_end_time - bronze_start_time);

EXCEPTION
	WHEN OTHERS THEN
		RAISE NOTICE '=========================';
		RAISE NOTICE 'ERROR OCCURED DURING LOADING BRONZE LAYER';
		RAISE NOTICE 'ERROR: %', SQLERRM;
		RAISE NOTICE '=========================';
END;
$$;
