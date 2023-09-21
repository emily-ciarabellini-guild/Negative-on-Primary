------------------------------------------------------------------------------------------------
-----Negative primary transaction queries-------------------------------------------------------
------------------------------------------------------------------------------------------------
--committed line items in MLB
SELECT 
    STLI.NET_TA*.01 as NET_TA_$, 
    PD.EMPLOYER_PAYMENT_OBLIGATION *.01 as EPO_$, 
    PD.STUDENT_PAYMENT_OBLIGATION*.01 as STUDENT_BILL_$,
    PD.GUILD_PAYMENT_OBLIGATION*.01 as GPO_$,
    PD.PAYMENT_REASON, 
    STLI.TERM_CODE, 
    STLI.GUILD_UUID, 
    STLI.PARTNER_STUDENT_ID, 
    AP.NAME as AP_NAME,
    STLI.UPDATED_AT, 
    STLI.ID AS STLI_ID
FROM TA_ORCHESTRATOR_PUBLIC.STUDENT_TERM_LINE_ITEMS STLI
JOIN TA_ORCHESTRATOR_PUBLIC.PAYMENT_DECISIONS PD on PD.ID = STLI.CURRENT_PAYMENT_DECISION_ID
JOIN ACADEMIC_SERVICE_V2_PUBLIC.ACADEMIC_PARTNER AP ON AP.ID = STLI.ACADEMIC_PARTNER_ID
WHERE CURRENT_STATE_NAME = 'Committed'
AND NET_TA != 0