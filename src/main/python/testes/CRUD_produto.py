# main_produto.py

import asyncio
from config.mongo_config import init
from models.produto import Produto
from repositories.repositorio_produto import RepositorioProduto

class ProdutoCRUD:
    def __init__(self):
        self.running = True
        self.repo = RepositorioProduto()

    async def mostrar_menu(self):
        print("\n" + "="*50)
        print("           SISTEMA DE PRODUTOS")
        print("="*50)
        print("1. 📋 Listar todos os produtos")
        print("2. 🔍 Buscar produto por ID")
        print("3. ➕ Criar novo produto")
        print("4. ✏️  Atualizar produto")
        print("5. 🗑️  Deletar produto")
        print("0. ❌ Sair")
        print("="*50)

    async def listar_produtos_menu(self):
        print("\n📋 LISTANDO TODOS OS PRODUTOS...")
        produtos = await self.repo.listar_todos()
        
        if not produtos:
            print("❌ Nenhum produto encontrado.")
            return
        
        print(f"\n✅ Encontrados {len(produtos)} produto(s):")
        print("-" * 80)
        for i, produto in enumerate(produtos, 1):
            print(f"{i}.\t{produto}")
        print("-" * 80)

    async def buscar_produto_menu(self):
        print("\n🔍 BUSCAR PRODUTO POR ID")
        print("💡 Dica: O ID deve ter 24 caracteres (ex: 507f1f77bcf86cd799439011)")
        produto_id = input("Digite o ID do produto: ").strip()
        
        if not produto_id:
            print("❌ ID não pode estar vazio.")
            return
        
        produto = await self.repo.buscar_por_id(produto_id)
        if produto:
            print(f"\n✅ Produto encontrado:")
            print(f"   {produto}")
        else:
            print("❌ Produto não encontrado ou ID inválido.")

    async def criar_produto_menu(self):
        print("\n➕ CRIAR NOVO PRODUTO")
        
        try:
            nome = input("Nome do produto: ").strip()
            if not nome:
                print("❌ Nome não pode estar vazio.")
                return
            
            descricao = input("Descrição: ").strip()
            if not descricao:
                print("❌ Descrição não pode estar vazia.")
                return
            
            preco_str = input("Preço (R$): ").strip()
            preco = float(preco_str.replace("R$", "").replace(",", "."))
            if preco < 0:
                print("❌ Preço não pode ser negativo.")
                return
            
            estoque_str = input("Quantidade em estoque: ").strip()
            estoque = int(estoque_str)
            if estoque < 0:
                print("❌ Estoque não pode ser negativo.")
                return
            
            categoria = input("Categoria: ").strip()
            if not categoria:
                print("❌ Categoria não pode estar vazia.")
                return
            
            produto = Produto(
                nome=nome,
                descricao=descricao,
                preco=preco,
                estoque=estoque,
                categoria=categoria
            )
            
            produto_criado = await self.repo.criar(produto)
            print(f"\n✅ Produto criado com sucesso!")
            print(f"   {produto_criado}")
            
        except ValueError:
            print("❌ Valor inválido! Preço e estoque devem ser números.")
        except Exception as e:
            print(type(e), e)
            print(f"❌ Erro ao criar produto: {e}")

    async def atualizar_produto_menu(self):
        print("\n✏️  ATUALIZAR PRODUTO")
        print("💡 Dica: O ID deve ter 24 caracteres (ex: 507f1f77bcf86cd799439011)")
        produto_id = input("Digite o ID do produto: ").strip()
        
        if not produto_id:
            print("❌ ID não pode estar vazio.")
            return
        
        produto = await self.repo.buscar_por_id(produto_id)
        if not produto:
            print("❌ Produto não encontrado ou ID inválido.")
            return
        
        print(f"\nProduto atual: {produto}")
        print("\n--- O que deseja atualizar? (deixe em branco para manter) ---")
        
        updates = {}
        
        novo_nome = input(f"Novo nome (atual: {produto.nome}): ").strip()
        if novo_nome:
            updates["nome"] = novo_nome
        
        nova_descricao = input(f"Nova descrição (atual: {produto.descricao}): ").strip()
        if nova_descricao:
            updates["descricao"] = nova_descricao
        
        novo_preco = input(f"Novo preço (atual: R$ {produto.preco:.2f}): ").strip()
        if novo_preco:
            try:
                preco = float(novo_preco.replace("R$", "").replace(",", "."))
                if preco < 0:
                    print("⚠️  Preço inválido, mantendo o anterior.")
                else:
                    updates["preco"] = preco
            except ValueError:
                print("⚠️  Preço inválido, mantendo o anterior.")
        
        novo_estoque = input(f"Novo estoque (atual: {produto.estoque}): ").strip()
        if novo_estoque:
            try:
                estoque = int(novo_estoque)
                if estoque < 0:
                    print("⚠️  Estoque inválido, mantendo o anterior.")
                else:
                    updates["estoque"] = estoque
            except ValueError:
                print("⚠️  Estoque inválido, mantendo o anterior.")
        
        nova_categoria = input(f"Nova categoria (atual: {produto.categoria}): ").strip()
        if nova_categoria:
            updates["categoria"] = nova_categoria
        
        if not updates:
            print("❌ Nenhuma alteração foi feita.")
            return
        
        try:
            produto_atualizado = await self.repo.atualizar_por_id(produto_id, updates)
            if produto_atualizado:
                print(f"\n✅ Produto atualizado com sucesso!")
                print(f"   {produto_atualizado}")
            else:
                print("❌ Erro ao atualizar produto.")
        except Exception as e:
            print(f"❌ Erro ao atualizar: {e}")

    async def deletar_produto_menu(self):
        print("\n🗑️  DELETAR PRODUTO")
        print("💡 Dica: O ID deve ter 24 caracteres (ex: 507f1f77bcf86cd799439011)")
        produto_id = input("Digite o ID do produto: ").strip()
        
        if not produto_id:
            print("❌ ID não pode estar vazio.")
            return
        
        produto = await self.repo.buscar_por_id(produto_id)
        if not produto:
            print("❌ Produto não encontrado ou ID inválido.")
            return
        
        print(f"\nProduto a ser deletado:")
        print(f"   {produto}")
        
        confirmacao = input("\n⚠️  Tem certeza? Esta ação não pode ser desfeita! (s/N): ").strip().lower()
        
        if confirmacao in ['s', 'sim', 'y', 'yes']:
            sucesso = await self.repo.deletar_por_id(produto_id)
            if sucesso:
                print("✅ Produto deletado com sucesso!")
            else:
                print("❌ Erro ao deletar produto.")
        else:
            print("❌ Operação cancelada.")

    async def executar(self):
        print("🚀 Inicializando sistema...")
        await init()
        print("✅ Conectado ao banco de dados!")
        
        while self.running:
            await self.mostrar_menu()
            
            try:
                opcao = input("\nEscolha uma opção: ").strip()
                
                if opcao == "1":
                    await self.listar_produtos_menu()
                elif opcao == "2":
                    await self.buscar_produto_menu()
                elif opcao == "3":
                    await self.criar_produto_menu()
                elif opcao == "4":
                    await self.atualizar_produto_menu()
                elif opcao == "5":
                    await self.deletar_produto_menu()
                elif opcao == "0":
                    print("\n👋 Encerrando sistema...")
                    self.running = False
                else:
                    print("❌ Opção inválida! Tente novamente.")
                
                if self.running and opcao != "0":
                    input("\nPressione ENTER para continuar...")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Sistema encerrado pelo usuário.")
                break
            except Exception as e:
                print(f"\n❌ Erro inesperado: {e}")
                input("Pressione ENTER para continuar...")

async def main():
    crud = ProdutoCRUD()
    await crud.executar()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
