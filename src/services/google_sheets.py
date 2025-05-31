import os
import pickle
import logging
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from src.utils.config import SCOPES, SPREADSHEET_ID, CATEGORIES_RANGE, EXPENSES_RANGE, INCOME_RANGE

logger = logging.getLogger(__name__)

def get_google_sheets_service():
    creds = None
    if os.path.exists('token.pickle'):
        try:
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
                logger.info("Token carregado com sucesso do arquivo")
        except Exception as e:
            logger.error(f"Erro ao carregar token: {str(e)}")
            creds = None
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                logger.info("Tentando atualizar token expirado")
                creds.refresh(Request())
                logger.info("Token atualizado com sucesso")
            except Exception as e:
                logger.error(f"Erro ao atualizar token: {str(e)}")
                creds = None
        
        if not creds:
            try:
                logger.info("Iniciando novo fluxo de autenticação")
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                
                # Gera a URL de autorização
                auth_url, _ = flow.authorization_url(
                    access_type='offline',
                    include_granted_scopes='true'
                )
                logger.info(f"URL de autorização gerada: {auth_url}")
                
                # Solicita o código de autorização
                print("\nPor favor, acesse a URL abaixo e autorize o aplicativo:")
                print(auth_url)
                print("\nDepois de autorizar, copie o código de autorização e cole aqui:")
                code = input("Código de autorização: ").strip()
                
                # Troca o código pelo token
                flow.fetch_token(code=code)
                creds = flow.credentials
                
                # Salva o token
                with open('token.pickle', 'wb') as token:
                    pickle.dump(creds, token)
                logger.info("Novo token gerado e salvo com sucesso")
                
            except Exception as e:
                logger.error(f"Erro durante a autenticação: {str(e)}")
                raise

    return build('sheets', 'v4', credentials=creds)

async def get_user_categories(user_id):
    service = get_google_sheets_service()
    sheet = service.spreadsheets()
    
    try:
        result = sheet.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=CATEGORIES_RANGE
        ).execute()
        
        values = result.get('values', [])
        categories = []
        
        for row in values:
            if len(row) >= 2 and str(row[0]) == str(user_id):
                categories.append(row[1])
        
        return categories
    except Exception as e:
        logger.error(f"Erro ao buscar categorias: {str(e)}")
        return []

async def add_category(user_id, category):
    service = get_google_sheets_service()
    sheet = service.spreadsheets()
    
    try:
        values = [[str(user_id), category]]
        body = {'values': values}
        
        sheet.values().append(
            spreadsheetId=SPREADSHEET_ID,
            range=CATEGORIES_RANGE,
            valueInputOption='RAW',
            body=body
        ).execute()
        return True
    except Exception as e:
        logger.error(f"Erro ao adicionar categoria: {str(e)}")
        return False

async def save_expense(user_id, data):
    service = get_google_sheets_service()
    sheet = service.spreadsheets()
    
    try:
        if data['metodo_pagamento'].lower() == 'crédito':
            installments = data['parcelas']
            total_value = round(data['valor_total'], 2)
            installment_value = round(total_value / installments, 2)
            
            # Ajusta o valor total para garantir que a soma das parcelas seja igual ao valor total
            adjusted_value = installment_value * installments
            difference = total_value - adjusted_value
            
            for i in range(installments):
                installment_date = datetime.strptime(data['data'], '%d/%m/%Y')
                # Calcula o novo mês e ano
                new_month = installment_date.month + i
                new_year = installment_date.year + (new_month - 1) // 12
                new_month = ((new_month - 1) % 12) + 1
                
                # Ajusta o dia para o último dia do mês se necessário
                if new_month == 12:
                    # Se for dezembro, o último dia é 31
                    last_day = 31
                else:
                    # Para outros meses, calcula o último dia usando o primeiro dia do próximo mês
                    last_day = (installment_date.replace(year=new_year, month=new_month + 1, day=1) - timedelta(days=1)).day
                
                new_day = min(installment_date.day, last_day)
                installment_date = installment_date.replace(year=new_year, month=new_month, day=new_day)
                
                # Ajusta o valor da última parcela para compensar a diferença de arredondamento
                final_value = installment_value
                if i == installments - 1 and difference != 0:
                    final_value = round(installment_value + difference, 2)
                
                values = [[
                    user_id,
                    data['descricao'],
                    data['categoria'],
                    installment_date.strftime('%d/%m/%Y'),
                    data['metodo_pagamento'],
                    f'{i+1}/{installments}',
                    total_value,
                    final_value
                ]]
                
                body = {'values': values}
                sheet.values().append(
                    spreadsheetId=SPREADSHEET_ID,
                    range=EXPENSES_RANGE,
                    valueInputOption='RAW',
                    body=body
                ).execute()
        else:
            values = [[
                user_id,
                data['descricao'],
                data['categoria'],
                data['data'],
                data['metodo_pagamento'],
                '1/1',
                round(data['valor_total'], 2),
                round(data['valor_total'], 2)
            ]]
            
            body = {'values': values}
            sheet.values().append(
                spreadsheetId=SPREADSHEET_ID,
                range=EXPENSES_RANGE,
                valueInputOption='RAW',
                body=body
            ).execute()
        return True
    except Exception as e:
        logger.error(f"Erro ao salvar despesa: {str(e)}")
        return False

async def save_income(user_id, data):
    service = get_google_sheets_service()
    sheet = service.spreadsheets()
    
    try:
        values = [[
            user_id,
            data['descricao'],
            data['categoria'],
            data['data'],
            data['valor_total']
        ]]
        
        body = {'values': values}
        sheet.values().append(
            spreadsheetId=SPREADSHEET_ID,
            range=INCOME_RANGE,
            valueInputOption='RAW',
            body=body
        ).execute()
        return True
    except Exception as e:
        logger.error(f"Erro ao salvar receita: {str(e)}")
        return False 