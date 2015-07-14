#coding: utf8 

favicon_path = '/static/img/favicon.ico'
companyType = {
                "en": ['Public', 'Private', 'Nonprofit'],
                "es": ['Pública', 'Privada', 'Sin Fines de Lucro']
            }
business_models = {
                    "en": [
                        'Business to Business', 'Business to Consumer', 
                        'Business to Government'],
                    "es": [
                        'Empresa a Empresa', 'Empresa a Consumidor', 
                        'Empresa a Gobierno']
                }
revenueSource = {
                "en": [
                    "Advertising", "Consulting", "Contributions/Donations", 
                    "Data analysis for clients", "Database licensing", 
                    "Government contract", "Lead generation to other businesses", 
                    "Membership fees", "Philanthropic grants", 
                    "Software licensing", "Subscriptions", 
                    "User fees for web or mobile access"],
                "au": [
                    "Advertising", "Consulting", "Contributions/Donations", 
                    "Data analysis for clients", "Database licensing", 
                    "Government contract", "Lead generation to other businesses", 
                    "Membership fees", "Philanthropic grants", 
                    "Software licensing", "Subscriptions", 
                    "User fees for web or mobile access"],
                "es": [
                    "Análisis de datos", "Consultoría", 
                    "Contratos gubernamentales", "Contribuciones/Donaciones", 
                    "Tarifas para el servicio móvil/internet", "Filantropía", 
                    "Generación de clientes", "Licencias de software", 
                    "Licencias de bases de datos", "Cuotas de membresía", 
                    "Publicidad", "Suscripciones"]
            }
datatypes = ['Federal Open Data', 'State Open Data', 'City/Local Open Data']
categories = {
                "en": {
                    "us": [
                        'Business & Legal Services', 'Data/Technology', 
                        'Education', 'Energy', 'Environment & Weather', 
                        'Finance & Investment', 'Food & Agriculture', 
                        'Geospatial/Mapping', 'Governance', 'Healthcare', 
                        'Housing/Real Estate', 'Insurance', 'Lifestyle & Consumer', 
                        'Media', 'Research & Consulting', 'Scientific Research', 
                        'Transportation'],
                    "mx": [
                        'Business Services', 'Data/Technology', 
                        'Education', 'Energy', 'Environment & Weather', 
                        'Finance & Investment', 'Food & Agriculture', 
                        'Geospatial/Mapping', 'Governance', 'Healthcare', 
                        'Housing/Real Estate', 'Insurance', 'Legal Services', 
                        'Lifestyle & Consumer', 'Media & Communications', 
                        'Research & Consulting', 'Scientific Research', 
                        'Transportation'],
                    "au": [
                        'Business & Legal Services', 'Data/Technology', 
                        'Education', 'Energy', 'Environment & Weather', 
                        'Finance & Investment', 'Food & Agriculture', 
                        'Geospatial/Mapping', 'Mining/Manufacturing', 
                        'Healthcare', 'Housing/Real Estate', 'Insurance', 
                        'Lifestyle & Consumer', 'Media', 'Research & Consulting', 
                        'Telecommunications / ISP\'s', 'Transportation']
                },
                "es": {
                    "mx": [
                        "Agricultura y Alimentación", "Vivienda/Bienes Raíces", 
                        "Clima y Medio Ambiente", "Educación", "Energía", 
                        "Estilos de vida y Consumidores", "Finanzas e Inversiones", 
                        "Gobierno", "Investigación Científica", 
                        "Investigación y Consultoría", "Mapeo/Geoespacial", 
                        "Medios y Comunicación", "Salud", "Seguros", 
                        "Servicios Legales", "Servicios Empresariales", 
                        "Tecnología/Datos", "Transporte"]
                }
            }
social_impacts = {
                "en": {
                    "us": [
                        'Citizen engagement and participation', 
                        'Consumer empowerment', 'Educational opportunity', 
                        'Environment and climate change', 'Financial access', 
                        'Food access and supply', 'Good governance', 
                        'Healthcare access', 'Housing access', 'Public safety'],
                    "au": [
                        'Citizen engagement and participation', 
                        'Consumer empowerment', 'Educational opportunity', 
                        'Environment and climate change', 'Financial access', 
                        'Food access and supply', 'Good governance', 
                        'Healthcare access', 'Housing access', 'Public safety'],
                    "mx": [
                        'Citizen engagement and participation', 
                        'Consumer empowerment', 'Educational opportunity', 
                        'Environment and climate change', 'Financial access', 
                        'Food access and supply', 'Good governance', 
                        'Healthcare access', 'Housing access', 'Public safety']
                },
                "es": {
                    "mx":[
                        "Acceso a la salud", "Acceso a la vivienda", 
                        "Acceso financiero", "Acceso y suministro de alimentos", 
                        '"Buen Gobierno"', "Empoderamiento al consumidor", 
                        "Medio ambiente y cambio climático", 
                        "Oportunidades educacionales", "Participación ciudadana", 
                        "Seguridad pública"]
                }
            }
data_types = {
                "en": {
                    "us": [
                        "Agriculture & Food", "Business", "Consumer", 
                        "Demographics & Social", "Economics", "Education", 
                        "Energy", "Environment", "Finance", "Geospatial/Mapping", 
                        "Government Operations", "Health/Healthcare", "Housing", 
                        "International/Global Development", "Legal", "Manufacturing", 
                        "Science and Research", "Public Safety", "Tourism", 
                        "Transportation", "Weather"],
                    "au":[
                        "Agriculture & Food", "Business", "Consumer", 
                        "Demographics & Social", "Economics", "Education", 
                        "Energy", "Environment", "Finance", "Geospatial/Mapping", 
                        "Government Operations", "Health/Healthcare", "Housing", 
                        "International/Global Development", "Legal", "Manufacturing", 
                        "Positioning/GPS", "Science and Research", "Public Safety", 
                        "Tourism", "Transportation", "Weather"],
                    "mx":[
                        "Agriculture & Food", "Business", "Consumer", 
                        "Demographics & Social", "Economics", "Education", 
                        "Energy", "Environment", "Finance", "Geospatial/Mapping", 
                        "Government Operations", "Health/Healthcare", "Housing", 
                        "International/Global Development", "Legal", "Manufacturing", 
                        "Science and Research", "Public Safety", "Tourism", 
                        "Transportation", "Weather"]
                },
                "es": {
                    "mx": [
                        "Agricultura y Alimentación", "Ciencia e investigación", 
                        "Clima", "Consumidor", "Demografía y Población", 
                        "Desarrollo internacional", "Economía", "Educación", 
                        "Empresas", "Energía", "Finanzas", "Legal", "Manufactura",
                        "Mapeo/Geoespacial", "Medio Ambiente", 
                        "Operaciones gubernamentales", "Salud", 
                        "Seguridad pública", "Transporte", "Turismo", "Vivienda"]
                }
            }
data_impacts = {
                "en": {
                    "us": [
                        "Cost efficiency", "New or improved product/service", 
                        "Job growth", "Revenue growth", "Identify new opportunities", 
                        "New/improved research"],
                    "au": [
                        "Cost efficiency", "New or improved product/service", 
                        "Job growth", "Revenue growth", "Identify new opportunities", 
                        "New/improved research"],
                    "mx": [
                        "Cost efficiency", "New or improved product/service", 
                        "Job growth", "Revenue growth", "Identify new opportunities", 
                        "New/improved research"],
                },
                "es": {
                    "mx": [
                        "Eficiencia económica", 
                        "Servicios/productos nuevos o mejorados", 
                        "Crecimiento de empleo", "Crecimiento de las ganancias", 
                        "Identificación de nuevas oportunidades", 
                        "Nuevas / mejoradas Investigaciones"]
                }
            }

source_count = ['1-10', '11-50', '51-100', '101+']
full_time_employees = [
                    '1-10', '11-50', '51-200', '201-500', '501-1,000', 
                    '1,001-5,000', '5,001-10,000', '10,001+']

states ={ 
            "us": {
                "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", 
                "AR": "Arkansas", "CA": "California", "CO": "Colorado", 
                "CT": "Connecticut", "DE": "Delaware", "DC": "District of Columbia", 
                "FL": "Florida", "GA": "Georgia", "HI": "Hawaii", "ID": "Idaho", 
                "IL": "Illinois", "IN": "Indiana", "IA": "Iowa", "KA": "Kansas", 
                "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", 
                "MD": "Maryland", "MA": "Massachusetts", "MI": "Michigan", 
                "MN": "Minnesota", "MS": "Mississippi", "MO": "Missouri", 
                "MT": "Montana", "NE": "Nebraska", "NV": "Nevada", 
                "NH": "New Hampshire", "NJ": "New Jersey", "NM": "New Mexico", 
                "NY": "New York", "NC": "North Carolina", "ND": "North Dakota", 
                "OH": "Ohio", "OK": "Oklahoma", "OR": "Oregon", 
                "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina", 
                "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas", 
                "UT": "Utah", "VT": "Vermont", "VA": "Virginia", "WA": "Washington", 
                "WV": "West Virginia", "WI": "Wisconsin", "WY": "Wyoming", 
                "PR": "Puerto Rico"},
            "mx": {
                "AS":"Aguascalientes", "BC":"Baja California", 
                "BS":"Baja California Sur", "CC":"Campeche", "CS":"Chiapas", 
                "CH":"Chihuahua", "CL":"Coahuila", "CM":"Colima", 
                "DF":"Distrito Federal", "DG":"Durango", "GT":"Guanajuato", 
                "GR":"Guerrero", "HG":"Hidalgo", "JC":"Jalisco", 
                "MC":"Estado de México", "MN":"Michoacán", "MS":"Morelos", 
                "NT":"Nayarit", "NL":"Nuevo León", "OC":"Oaxaca", "PL":"Puebla", 
                "QT":"Querétaro", "QR":"Quintana Roo", "SP":"San Luis Potosí", 
                "SL":"Sinaloa", "SR":"Sonora", "TC":"Tabasco", "TS":"Tamaulipas", 
                "TL":"Tlaxcala", "VZ":"Veracruz", "YN":"Yucatán", "ZS":"Zacatecas"},
            "au": {
                "ACT":"Australian Capital Territory", "NSW":"New South Wales", 
                "NT":"Northern Territory", "QLD":"Queensland", 
                "SA":"South Australia", "TAS":"Tasmania", "VIC":"Victoria", 
                "WA":"Western Australia"}
        }
stateListAbbrev = { 
            "us": [
                "", "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "DC", "FL", 
                "GA", "HI", "ID", "IL", "IN", "IA", "KA", "KY", "LA", "ME", "MD", 
                "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", 
                "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", 
                "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY", "PR"],
            "ca": [
                "", "AB", "BC", "MB", "NB", "NL", "NT", "NS", "NU", "ON", "PE", 
                "QC", "SK", "YT"],
            "au": [
                "", "ACT", "NSW", "NT", "QLD", "SA", "TAS", "VIC", "WA"],
            "mx": [
                "", "AS", "BC", "BS", "CC", "CS", "CH", "CL", "CM", "DF", "DG", 
                "MC", "GT", "GR", "HG", "JC", "MN", "MS", "NT", "NL", "OC", "PL", 
                "QT", "QR", "SP", "SL", "SR", "TC", "TS", "TL", "VZ", "YN", "ZS"]
            }
stateList = {
            "us": [
                "(Select State)", "Alabama", "Alaska", "Arizona", "Arkansas", 
                "California", "Colorado", "Connecticut", "Delaware", 
                "District of Columbia", "Florida", "Georgia", "Hawaii", "Idaho", 
                "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", 
                "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", 
                "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", 
                "New Hampshire", "New Jersey", "New Mexico", "New York", 
                "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", 
                "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", 
                "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", 
                "West Virginia", "Wisconsin", "Wyoming", "Puerto Rico"],
            "ca": [
                "(Select Province/Territory)", "Alberta", "British Columbia", 
                "Manitoba", "New Brunswick", "Newfoundland and Labrador", 
                "Northwest Territories", "Nova Scotia", "Nunavut", "Ontario", 
                "Prince Edward Island", "Quebec", "Saskatchewan", "Yukon"],
            "au": [
                "(Select Province/Territory)", "Australian Capital Territory", 
                "New South Wales", "Northern Territory", "Queensland", 
                "South Australia", "Tasmania", "Victoria", "Western Australia"],
            "mx": [
                "(Seleccione un Estado)", "Aguascalientes", "Baja California", 
                "Baja California Sur", "Campeche", "Chiapas", "Chihuahua", 
                "Coahuila", "Colima", "Distrito Federal", "Durango", 
                "Estado de México", "Guanajuato", "Guerrero", "Hidalgo", 
                "Jalisco", "Michoacán", "Morelos", "Nayarit", "Nuevo León", 
                "Oaxaca", "Puebla", "Querétaro", "Quintana Roo", 
                "San Luis Potosí", "Sinaloa", "Sonora", "Tabasco", "Tamaulipas", 
                "Tlaxcala", "Veracruz", "Yucatán", "Zacatecas"]
            }
agency_types = ['Federal','State','City/County','University/Institution']
available_countries = ["us", "au", "mx", "fr", "kr", "it"]
disabled_countries = []
country_keys = { 
    "us":"United States", "au":"Australia", "United States":"us", 
    "Australia":"au",  "Mexico":"mx", "mx":"Mexico", "it": "Italy"}

# "fields" include text fields, textareas, drop-down menus
company_contact_fields = ['firstName', 'lastName', 'title', 'email', 'phone']
company_fields = [
    'companyName', 'url', 'yearFounded', 'city', 'state', 'zipCode', 
    'description', 'descriptionShort', 'financialInfo', 'notes']
company_fields_validators = {
    'yearFounded': lambda x: int(x) >= 1000
}
company_fields_checkboxes = ['revenueSource', 'businessModel', 'socialImpact']
company_fields_radio_buttons = ['companyCategory', 'companyType', 'fte']
company_data_fields = ['dataComments', 'exampleUses', 'dataWishlist']
company_data_checkboxes = ['dataTypes', 'dataImpacts']
company_data_radio_buttons = ['sourceCount']
company_admin_booleans = [
    'display', 'submittedSurvey','vetted', 'vettedByCompany', 
    'submittedThroughWebsite', 'locked']

abbreviations = { 
    "us":[
        {"Department":"Dept."},
        {"Administration": "Admin."},
        {"United States":"US"},
        {"U.S.":"US"},
        {"National":"Nat'l"},
        {"Federal":"Fed."},
        {"Commission":"Com."},
        {"International":"Int'l"},
        {"Development":"Dev."},
        {"Corporation":"Corp"},
        {"Institute":"Inst."},
        {"Administrative":"Admin."},
        {" and ":" & "},
        {"Financial":"Fin"},
        {"Environmental":"Env."},
        {"Protection":"Prot."}
    ],
    "mx":[
        {"Secretaría":"Sec."},
        {"Instituto":"Inst."},
        {"Comunicaciones":"Com."},
        {"Federal":"Fed."},
        {"Nacional":"Nal."},
        {"República":"Rep."},
        {"Comisión":"Com."},
        {"General":"Gral."},
        {"Ambiente":"Amb."},
        {"Consumidores":"Cons."}
    ],
    "au":[
        {"Department":"Dept."},
        {"Administration": "Admin."},
        {"United States":"US"},
        {"U.S.":"US"},
        {"National":"Nat'l"},
        {"Federal":"Fed."},
        {"Commission":"Com."},
        {"International":"Int'l"},
        {"Development":"Dev."},
        {"Corporation":"Corp"},
        {"Institute":"Inst."},
        {"Administrative":"Admin."},
        {" and ":" & "},
        {"Financial":"Fin"},
        {"Environmental":"Env."},
        {"Protection":"Prot."}
    ],
}
