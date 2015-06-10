DROP TABLE DICT_UCI_ML_TENNIS;

CREATE TABLE DICT_UCI_ML_TENNIS AS
SELECT '2013####-M-'|| replace(TOURNAMENT,' ','_') || '-' || replace(PLAYER1,' ','_') || '-' || replace(PLAYER2,' ','_') AS UCI_ID1,
        '2013####-M-'|| replace(TOURNAMENT,' ','_') || '-' || replace(PLAYER2,' ','_') || '-' || replace(PLAYER1,' ','_') AS UCI_ID2,
        NULL AS ML_TENNIS_ID
FROM ALL_MATCHES;


SELECT *
FROM DICT_UCI_ML_TENNIS;

SELECT *
FROM 
        ML_Tennis.RAW_CHARTING_M_MATCHES AS ML 
    LEFT JOIN 
        DICT_UCI_ML_TENNIS AS DICT
        ON
            substr(ML.DATE,1,4) || '####-M-' || replace(ML.TOURNAMENT,' ','_') || '-' || replace(ML.PLAYER_1,' ','_') || '-' || replace(ML.PLAYER_2,' ','_') = DICT.UCI_ID1 OR substr(ML.DATE,1,4) || '####-M-' || replace(ML.TOURNAMENT,' ','_') || '-' || replace(ML.PLAYER_1,' ','_') || '-' || replace(ML.PLAYER_2,' ','_') = DICT.UCI_ID2
ORDER BY DICT.UCI_ID1 DESC
            

SELECT substr(ML.DATE,1,4) || '####-M-' || replace(TOURNAMENT,' ','_') || '-' || replace(PLAYER_1,' ','_') || '-' || replace(PLAYER_2,' ','_'),
        MATCH_ID
FROM 
        ML_Tennis.RAW_CHARTING_M_MATCHES AS ML 

--'20150415-M-Monte_Carlo_Masters-R32-Stanislas_Wawrinka-Juan_Monaco';


SELECT DISTINCT ROUND
FROM ALL_MATCHES;

SELECT DISTINCT ROUND
FROM ML_Tennis.RAW_CHARTING_M_MATCHES