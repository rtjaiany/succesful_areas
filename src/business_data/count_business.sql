CREATE TABLE business_status AS
SELECT 
    cod_cidade, 
    secao_cnae, 
    desc_secao,
    
    -- Count of active companies (Status '02')
    COUNT(CASE WHEN situacao_cadastral = '02' THEN 1 END) AS active_companies,
    
    -- Count of closed companies ('08') with reasons '01', '05', or '06'
    COUNT(CASE 
        WHEN situacao_cadastral = '08' 
        AND motivo_situacao_cadastral IN ('01', '05', '06') 
        THEN 1 
    END) AS closed_companies,
    
    -- Active Head Offices (Status '02' AND ID '1')
    COUNT(CASE 
        WHEN situacao_cadastral = '02' 
        AND identificador_matriz_filial = '1' 
        THEN 1 
    END) AS head_offices,
    
    -- Active Branches (Status '02' AND ID '2')
    COUNT(CASE 
        WHEN situacao_cadastral = '02' 
        AND identificador_matriz_filial = '2' 
        THEN 1 
    END) AS branches,
    
    -- Failed Head Offices (Status '08', specific reasons, and ID '1')
    COUNT(CASE 
        WHEN situacao_cadastral = '08' 
        AND motivo_situacao_cadastral IN ('01', '05', '06') 
        AND identificador_matriz_filial = '1' 
        THEN 1 
    END) AS failed_head_offices,
    
    -- Failed Branches (Status '08', specific reasons, and ID '2')
    COUNT(CASE 
        WHEN situacao_cadastral = '08' 
        AND motivo_situacao_cadastral IN ('01', '05', '06') 
        AND identificador_matriz_filial = '2' 
        THEN 1 
    END) AS failed_branches

FROM secoes
GROUP BY 
    cod_cidade, 
    secao_cnae, 
    desc_secao;