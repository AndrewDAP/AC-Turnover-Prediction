"""
Module to store the names of the stages of the ingestion pipeline.
"""


class IngestionPipelineStages:
    """
    Class to store the names of the stages of the ingestion pipeline.
    """

    VISIT_DATA_CLEANING_CALCULATED_FIELDS_STAGE = (
        "Visit_Data_Cleaning_Calculated_fields_Stage"
    )

    CLIENT_DATA_CLEANING_CALCULATED_FIELDS_STAGE = (
        "Client_Data_Cleaning_Calculated_fields_Stage"
    )

    EMPLOYEE_DATA_CLEANING_CALCULATED_FIELDS_STAGE = (
        "Employee_Data_Cleaning_Calculated_fields_Stage"
    )

    CLOCK_DATA_CLEANING_CALCULATED_FIELDS_STAGE = (
        "Clock_Data_Cleaning_Calculated_fields_Stage"
    )

    Y_LABELS_GENERATION_STAGE = "Y_Labels_Generation_Stage"

    AUGMENT_VISIT_STAGE = "Augmented_Visit_Stage"

    SEGMENTATION_STAGE = "Segmentation_Stage"

    EMPLOYEE_HISTORY_AGGREGATION_STAGE = "Employee_History_Aggregation_Stage"

    EMPLOYEE_HISTORY_FILL_GAPS_STAGE = "Employee_History_Fill_Gaps_Stage"

    EMPLOYEE_HISTORY_CALCULATED_FIELDS_STAGE = (
        "Employee_History_Calculated_Fields_Stage"
    )

    EMPLOYEE_HISTORY_ROLLING_FEATURES_STAGE = "Employee_History_Rolling_Features_Stage"

    EMPLOYEE_HISTORY_FILL_NA_STAGE = "Employee_History_Fill_Na_Stage"

    EMPLOYEE_HISTORY_ANOMALY_DETECTION_STAGE = (
        "Employee_History_Anomaly_Detection_Stage"
    )

    TRAINING_EMPLOYEE_HISTORY_STAGE = "Training_Employee_History_Stage"
