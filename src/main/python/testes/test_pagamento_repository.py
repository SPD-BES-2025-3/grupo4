# test_pagamento_repository.py

import pytest
import asyncio
import sys
import os
from datetime import datetime
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from faker import Faker

# Add the parent directory to Python path to import local modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.pagamento import Pagamento
from repositories.pagamento_repository import *

# Initialize Faker for generating test data
fake = Faker('pt_BR')

# Test database configuration
TEST_DATABASE_URL = os.getenv("TEST_MONGO_URI", "mongodb://localhost:27017/test_pagamentos_db")

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def beanie_initialized():
    client = AsyncIOMotorClient(TEST_DATABASE_URL)
    db = client.get_default_database()
    await init_beanie(database=db, document_models=[Pagamento])
    yield
    await client.drop_database(db.name)
    client.close()




@pytest.fixture
async def clean_database(beanie_initialized):  # ensures correct loop context
    await Pagamento.delete_all()
    yield
    await Pagamento.delete_all()

@pytest.mark.asyncio
async def test_database_connection(beanie_initialized):
    assert Pagamento is not None



@pytest.fixture
def pagamento_data():
    """Generate test payment data."""
    return {
        "dados_pagamento": f"Visa **** {fake.random_number(digits=4)} - {fake.random_number(digits=2, fix_len=True)}/{fake.random_number(digits=2, fix_len=True)}",
        "valor": round(fake.random.uniform(10.0, 1000.0), 2),
        "metodo": fake.random_element(elements=["cartao", "boleto", "pix", "paypal"])
    }

@pytest.fixture
async def sample_pagamento(clean_database, pagamento_data):
    """Create a sample payment for testing."""
    pagamento = Pagamento(**pagamento_data)
    await pagamento.insert()
    return pagamento

class TestPagamentoRepository:
    """Test suite for pagamento repository functions."""
    
    # Test validation functions
    @pytest.mark.unit
    def test_is_valid_object_id_valid(self):
        """Test valid ObjectId validation."""
        valid_id = "507f1f77bcf86cd799439011"
        assert is_valid_object_id(valid_id) is True
    
    @pytest.mark.unit
    def test_is_valid_object_id_invalid_length(self):
        """Test invalid ObjectId - wrong length."""
        invalid_id = "507f1f77bcf86cd"
        assert is_valid_object_id(invalid_id) is False
    
    @pytest.mark.unit
    def test_is_valid_object_id_invalid_characters(self):
        """Test invalid ObjectId - non-hex characters."""
        invalid_id = "507f1f77bcf86cd799439xyz"
        assert is_valid_object_id(invalid_id) is False
    
    @pytest.mark.unit
    def test_is_valid_object_id_none(self):
        """Test invalid ObjectId - None value."""
        assert is_valid_object_id(None) is False
    
    @pytest.mark.unit
    def test_is_valid_object_id_empty_string(self):
        """Test invalid ObjectId - empty string."""
        assert is_valid_object_id("") is False
    
    # Test CRUD operations
    @pytest.mark.asyncio
    async def test_criar_pagamento(self, clean_database, pagamento_data):
        """Test creating a new payment."""
        pagamento = Pagamento(**pagamento_data)
        
        created_pagamento = await criar_pagamento(pagamento)
        
        assert created_pagamento is not None
        assert created_pagamento.id is not None
        assert created_pagamento.dados_pagamento == pagamento_data["dados_pagamento"]
        assert created_pagamento.valor == pagamento_data["valor"]
        assert created_pagamento.metodo == pagamento_data["metodo"]
        assert created_pagamento.status == "pendente"  # Default status
    
    @pytest.mark.asyncio
    async def test_buscar_pagamento_exists(self, sample_pagamento):
        """Test finding an existing payment by ID."""
        found_pagamento = await buscar_pagamento(str(sample_pagamento.id))
        
        assert found_pagamento is not None
        assert found_pagamento.id == sample_pagamento.id
        assert found_pagamento.dados_pagamento == sample_pagamento.dados_pagamento
    
    @pytest.mark.asyncio
    async def test_buscar_pagamento_not_exists(self, clean_database):
        """Test finding a non-existing payment by ID."""
        fake_id = "507f1f77bcf86cd799439011"
        found_pagamento = await buscar_pagamento(fake_id)
        
        assert found_pagamento is None
    
    @pytest.mark.asyncio
    async def test_buscar_pagamento_invalid_id(self, clean_database):
        """Test finding payment with invalid ID."""
        invalid_id = "invalid_id"
        found_pagamento = await buscar_pagamento(invalid_id)
        
        assert found_pagamento is None
    
    @pytest.mark.asyncio
    async def test_listar_pagamentos_empty(self, clean_database):
        """Test listing payments when database is empty."""
        pagamentos = await listar_pagamentos()
        
        assert pagamentos == []
    
    @pytest.mark.asyncio
    async def test_listar_pagamentos_with_data(self, clean_database):
        """Test listing payments with data in database."""
        # Create multiple payments
        pagamentos_criados = []
        for i in range(3):
            pagamento_data = {
                "dados_pagamento": f"Test Card {i}",
                "valor": 100.0 * (i + 1),
                "metodo": "cartao"
            }
            pagamento = Pagamento(**pagamento_data)
            await pagamento.insert()
            pagamentos_criados.append(pagamento)
        
        pagamentos = await listar_pagamentos()
        
        assert len(pagamentos) == 3
        assert all(isinstance(p, Pagamento) for p in pagamentos)
    
    @pytest.mark.asyncio
    async def test_atualizar_pagamento(self, sample_pagamento):
        """Test updating a payment."""
        update_data = {
            "valor": 999.99,
            "status": "processado"
        }
        
        updated_pagamento = await atualizar_pagamento(str(sample_pagamento.id), update_data)
        
        assert updated_pagamento is not None
        assert updated_pagamento.valor == 999.99
        assert updated_pagamento.status == "processado"
        # Verify original data remains unchanged
        assert updated_pagamento.dados_pagamento == sample_pagamento.dados_pagamento
        assert updated_pagamento.metodo == sample_pagamento.metodo
    
    @pytest.mark.asyncio
    async def test_atualizar_pagamento_not_exists(self, clean_database):
        """Test updating a non-existing payment."""
        fake_id = "507f1f77bcf86cd799439011"
        update_data = {"valor": 999.99}
        
        result = await atualizar_pagamento(fake_id, update_data)
        
        assert result is None
    
    @pytest.mark.asyncio
    async def test_atualizar_pagamento_invalid_id(self, clean_database):
        """Test updating with invalid ID."""
        invalid_id = "invalid_id"
        update_data = {"valor": 999.99}
        
        result = await atualizar_pagamento(invalid_id, update_data)
        
        assert result is None
    
    @pytest.mark.asyncio
    async def test_atualizar_pagamento_completo(self, sample_pagamento):
        """Test updating a complete payment object."""
        sample_pagamento.valor = 777.77
        sample_pagamento.status = "falhou"
        
        updated_pagamento = await atualizar_pagamento_completo(sample_pagamento)
        
        assert updated_pagamento is not None
        assert updated_pagamento.valor == 777.77
        assert updated_pagamento.status == "falhou"
    
    @pytest.mark.asyncio
    async def test_atualizar_pagamento_completo_no_id(self, pagamento_data):
        """Test updating complete payment without ID."""
        pagamento = Pagamento(**pagamento_data)  # No ID set
        
        result = await atualizar_pagamento_completo(pagamento)
        
        assert result is None
    
    @pytest.mark.asyncio
    async def test_deletar_pagamento(self, sample_pagamento):
        """Test deleting a payment by ID."""
        pagamento_id = str(sample_pagamento.id)
        
        result = await deletar_pagamento(pagamento_id)
        
        assert result is True
        # Verify it's actually deleted
        found_pagamento = await buscar_pagamento(pagamento_id)
        assert found_pagamento is None
    
    @pytest.mark.asyncio
    async def test_deletar_pagamento_not_exists(self, clean_database):
        """Test deleting a non-existing payment."""
        fake_id = "507f1f77bcf86cd799439011"
        
        result = await deletar_pagamento(fake_id)
        
        assert result is False
    
    @pytest.mark.asyncio
    async def test_deletar_pagamento_invalid_id(self, clean_database):
        """Test deleting with invalid ID."""
        invalid_id = "invalid_id"
        
        result = await deletar_pagamento(invalid_id)
        
        assert result is False
    
    @pytest.mark.asyncio
    async def test_deletar_pagamento_objeto(self, sample_pagamento):
        """Test deleting a payment object."""
        pagamento_id = str(sample_pagamento.id)
        
        result = await deletar_pagamento_objeto(sample_pagamento)
        
        assert result is True
        # Verify it's actually deleted
        found_pagamento = await buscar_pagamento(pagamento_id)
        assert found_pagamento is None
    
    @pytest.mark.asyncio
    async def test_deletar_pagamento_objeto_no_id(self, pagamento_data):
        """Test deleting payment object without ID."""
        pagamento = Pagamento(**pagamento_data)  # No ID set
        
        result = await deletar_pagamento_objeto(pagamento)
        
        assert result is False
'''
class TestPagamentoUtilityFunctions:
    """Test suite for utility functions."""
    
    @pytest.mark.asyncio
    async def test_buscar_pagamentos_por_status(self, clean_database):
        """Test finding payments by status."""
        # Create payments with different statuses
        for status in ["pendente", "processado", "falhou"]:
            for i in range(2):  # 2 payments per status
                pagamento_data = {
                    "dados_pagamento": f"Test {status} {i}",
                    "valor": 100.0,
                    "metodo": "cartao",
                    "status": status
                }
                pagamento = Pagamento(**pagamento_data)
                await pagamento.insert()
        
        # Test each status
        pendentes = await buscar_pagamentos_por_status("pendente")
        processados = await buscar_pagamentos_por_status("processado")
        falharam = await buscar_pagamentos_por_status("falhou")
        
        assert len(pendentes) == 2
        assert len(processados) == 2
        assert len(falharam) == 2
        assert all(p.status == "pendente" for p in pendentes)
        assert all(p.status == "processado" for p in processados)
        assert all(p.status == "falhou" for p in falharam)
    
    @pytest.mark.asyncio
    async def test_buscar_pagamentos_por_metodo(self, clean_database):
        """Test finding payments by method."""
        # Create payments with different methods
        metodos = ["cartao", "boleto", "pix", "paypal"]
        for metodo in metodos:
            pagamento_data = {
                "dados_pagamento": f"Test {metodo}",
                "valor": 100.0,
                "metodo": metodo
            }
            pagamento = Pagamento(**pagamento_data)
            await pagamento.insert()
        
        # Test each method
        for metodo in metodos:
            pagamentos = await buscar_pagamentos_por_metodo(metodo)
            assert len(pagamentos) == 1
            assert pagamentos[0].metodo == metodo
    
    @pytest.mark.asyncio
    async def test_buscar_pagamentos_por_valor_minimo(self, clean_database):
        """Test finding payments by minimum value."""
        # Create payments with different values
        valores = [50.0, 100.0, 200.0, 500.0]
        for valor in valores:
            pagamento_data = {
                "dados_pagamento": f"Test {valor}",
                "valor": valor,
                "metodo": "cartao"
            }
            pagamento = Pagamento(**pagamento_data)
            await pagamento.insert()
        
        # Test minimum value filter
        pagamentos_150 = await buscar_pagamentos_por_valor_minimo(150.0)
        pagamentos_300 = await buscar_pagamentos_por_valor_minimo(300.0)
        
        assert len(pagamentos_150) == 2  # 200.0 and 500.0
        assert len(pagamentos_300) == 1  # 500.0
        assert all(p.valor >= 150.0 for p in pagamentos_150)
        assert all(p.valor >= 300.0 for p in pagamentos_300)
    
    @pytest.mark.asyncio
    async def test_contar_pagamentos(self, clean_database):
        """Test counting total payments."""
        # Initially empty
        count = await contar_pagamentos()
        assert count == 0
        
        # Add some payments
        for i in range(5):
            pagamento_data = {
                "dados_pagamento": f"Test {i}",
                "valor": 100.0,
                "metodo": "cartao"
            }
            pagamento = Pagamento(**pagamento_data)
            await pagamento.insert()
        
        count = await contar_pagamentos()
        assert count == 5
    
    @pytest.mark.asyncio
    async def test_contar_pagamentos_por_status(self, clean_database):
        """Test counting payments by status."""
        # Create payments with different statuses
        status_counts = {"pendente": 3, "processado": 2, "falhou": 1}
        
        for status, count in status_counts.items():
            for i in range(count):
                pagamento_data = {
                    "dados_pagamento": f"Test {status} {i}",
                    "valor": 100.0,
                    "metodo": "cartao",
                    "status": status
                }
                pagamento = Pagamento(**pagamento_data)
                await pagamento.insert()
        
        # Test counts
        for status, expected_count in status_counts.items():
            count = await contar_pagamentos_por_status(status)
            assert count == expected_count
'''
""" 
class TestPagamentoIntegration:
    '''Integration tests for complete workflows.'''
    
    @pytest.mark.asyncio
    async def test_complete_crud_workflow(self, clean_database):
        '''Test complete CRUD workflow'''
        # CREATE
        pagamento_data = {
            "dados_pagamento": "Visa **** 1234 - 12/25",
            "valor": 150.75,
            "metodo": "cartao"
        }
        pagamento = Pagamento(**pagamento_data)
        created_pagamento = await criar_pagamento(pagamento)
        
        assert created_pagamento.id is not None
        pagamento_id = str(created_pagamento.id)
        
        # READ
        found_pagamento = await buscar_pagamento(pagamento_id)
        assert found_pagamento is not None
        assert found_pagamento.valor == 150.75
        
        # UPDATE
        update_data = {"status": "processado", "valor": 175.50}
        updated_pagamento = await atualizar_pagamento(pagamento_id, update_data)
        assert updated_pagamento.status == "processado"
        assert updated_pagamento.valor == 175.50
        
        # DELETE
        delete_result = await deletar_pagamento(pagamento_id)
        assert delete_result is True
        
        # VERIFY DELETION
        deleted_pagamento = await buscar_pagamento(pagamento_id)
        assert deleted_pagamento is None
    
    @pytest.mark.asyncio
    async def test_bulk_operations_performance(self, clean_database):
        '''Test performance with bulk operations'''
        # Create multiple payments
        pagamentos = []
        for i in range(100):
            pagamento_data = {
                "dados_pagamento": f"Test Bulk {i}",
                "valor": 100.0 + i,
                "metodo": fake.random_element(elements=["cartao", "boleto", "pix", "paypal"]),
                "status": fake.random_element(elements=["pendente", "processado", "falhou"])
            }
            pagamento = Pagamento(**pagamento_data)
            await pagamento.insert()
            pagamentos.append(pagamento)
        
        # Test listing all
        all_pagamentos = await listar_pagamentos()
        assert len(all_pagamentos) == 100
        
        # Test counting
        total_count = await contar_pagamentos()
        assert total_count == 100
        
        # Test filtering
        cartao_pagamentos = await buscar_pagamentos_por_metodo("cartao")
        assert len(cartao_pagamentos) > 0
        
        high_value_pagamentos = await buscar_pagamentos_por_valor_minimo(150.0)
        assert len(high_value_pagamentos) > 0
"""
# Custom markers for test categorization
pytest_plugins = []

# Pytest configuration for this test file
def pytest_configure(config):
    """Configure pytest markers."""
    config.addinivalue_line("markers", "slow: marks tests as slow")
    config.addinivalue_line("markers", "integration: marks tests as integration tests")
    config.addinivalue_line("markers", "unit: marks tests as unit tests")

# Run specific test categories
# pytest test_pagamento_repository.py -m unit
# pytest test_pagamento_repository.py -m integration
# pytest test_pagamento_repository.py -m slow