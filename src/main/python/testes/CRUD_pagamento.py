# main.py

import asyncio
from config.mongo_config import init
from models.pagamento import Pagamento
from repositories.repositorio_pagamento import RepositorioPagamento

class PagamentoCRUD:
    def __init__(self):
        self.running = True
        self.repo = RepositorioPagamento()

    async def mostrar_menu(self):
        print("\n" + "="*50)
        print("           SISTEMA DE PAGAMENTOS")
        print("="*50)
        print("1. 📋 Listar todos os pagamentos")
        print("2. 🔍 Buscar pagamento por ID")
        print("3. ➕ Criar novo pagamento")
        print("4. ✏️  Atualizar pagamento")
        print("5. 🗑️  Deletar pagamento")
        print("6. 📊 Estatísticas")
        print("0. ❌ Sair")
        print("="*50)

    async def listar_pagamentos_menu(self):
        print("\n📋 LISTANDO TODOS OS PAGAMENTOS...")
        pagamentos = await self.repo.listar_todos()
        
        if not pagamentos:
            print("❌ Nenhum pagamento encontrado.")
            return
        
        print(f"\n✅ Encontrados {len(pagamentos)} pagamento(s):")
        print("-" * 80)
        for i, pagamento in enumerate(pagamentos, 1):
            print(f"{i}.\t{pagamento}")
        print("-" * 80)

    async def buscar_pagamento_menu(self):
        print("\n🔍 BUSCAR PAGAMENTO POR ID")
        print("💡 Dica: O ID deve ter 24 caracteres (ex: 507f1f77bcf86cd799439011)")
        pagamento_id = input("Digite o ID do pagamento: ").strip()
        
        if not pagamento_id:
            print("❌ ID não pode estar vazio.")
            return
        
        pagamento = await self.repo.buscar_por_id(pagamento_id)
        if pagamento:
            print(f"\n✅ Pagamento encontrado:")
            print(f"   {pagamento}")
        else:
            print("❌ Pagamento não encontrado ou ID inválido.")

    async def criar_pagamento_menu(self):
        print("\n➕ CRIAR NOVO PAGAMENTO")
        
        try:
            # Coletar dados do pagamento como string
            print("\n--- Dados do Cartão/Pagamento ---")
            dados_pagamento = input("Dados do pagamento (ex: Visa **** 1234 - 12/25): ").strip()
            
            if not dados_pagamento:
                print("❌ Dados do pagamento não podem estar vazios.")
                return
            
            print("\n--- Dados do Pagamento ---")
            valor_str = input("Valor (R$): ").strip()
            valor = float(valor_str.replace("R$", "").replace(",", "."))
            
            print("Métodos disponíveis: cartao, boleto, pix, paypal")
            metodo = input("Método de pagamento: ").strip().lower()
            
            if metodo not in ["cartao", "boleto", "pix", "paypal"]:
                print("❌ Método inválido!")
                return
            
            # Criar pagamento
            pagamento = Pagamento(
                dados_pagamento=dados_pagamento,
                valor=valor,
                metodo=metodo
            )
            
            # Salvar no banco
            pagamento_criado = await self.repo.criar(pagamento)
            print(f"\n✅ Pagamento criado com sucesso!")
            print(f"   {pagamento_criado}")
            
        except ValueError:
            print("❌ Valor inválido! Use apenas números.")
        except Exception as e:
            print(f"❌ Erro ao criar pagamento: {e}")

    async def atualizar_pagamento_menu(self):
        print("\n✏️  ATUALIZAR PAGAMENTO")
        print("💡 Dica: O ID deve ter 24 caracteres (ex: 507f1f77bcf86cd799439011)")
        pagamento_id = input("Digite o ID do pagamento: ").strip()
        
        if not pagamento_id:
            print("❌ ID não pode estar vazio.")
            return
        
        # Verificar se existe
        pagamento = await self.repo.buscar_por_id(pagamento_id)
        if not pagamento:
            print("❌ Pagamento não encontrado ou ID inválido.")
            return
        
        print(f"\nPagamento atual: {pagamento}")
        print("\n--- O que deseja atualizar? (deixe em branco para manter) ---")
        
        updates = {}
        
        # Dados do pagamento
        novos_dados = input(f"Novos dados do pagamento (atual: {pagamento.dados_pagamento}): ").strip()
        if novos_dados:
            updates["dados_pagamento"] = novos_dados
        
        # Valor
        novo_valor = input(f"Novo valor (atual: R$ {pagamento.valor:.2f}): ").strip()
        if novo_valor:
            try:
                updates["valor"] = float(novo_valor.replace("R$", "").replace(",", "."))
            except ValueError:
                print("⚠️  Valor inválido, mantendo o anterior.")
        
        # Status
        print("Status disponíveis: pendente, processado, falhou")
        novo_status = input(f"Novo status (atual: {pagamento.status}): ").strip().lower()
        if novo_status and novo_status in ["pendente", "processado", "falhou"]:
            updates["status"] = novo_status
        elif novo_status:
            print("⚠️  Status inválido, mantendo o anterior.")
        
        # Método
        print("Métodos disponíveis: cartao, boleto, pix, paypal")
        novo_metodo = input(f"Novo método (atual: {pagamento.metodo}): ").strip().lower()
        if novo_metodo and novo_metodo in ["cartao", "boleto", "pix", "paypal"]:
            updates["metodo"] = novo_metodo
        elif novo_metodo:
            print("⚠️  Método inválido, mantendo o anterior.")
        
        if not updates:
            print("❌ Nenhuma alteração foi feita.")
            return
        
        try:
            pagamento_atualizado = await self.repo.atualizar_por_id(pagamento_id, updates)
            if pagamento_atualizado:
                print(f"\n✅ Pagamento atualizado com sucesso!")
                print(f"   {pagamento_atualizado}")
            else:
                print("❌ Erro ao atualizar pagamento.")
        except Exception as e:
            print(f"❌ Erro ao atualizar: {e}")

    async def deletar_pagamento_menu(self):
        print("\n🗑️  DELETAR PAGAMENTO")
        print("💡 Dica: O ID deve ter 24 caracteres (ex: 507f1f77bcf86cd799439011)")
        pagamento_id = input("Digite o ID do pagamento: ").strip()
        
        if not pagamento_id:
            print("❌ ID não pode estar vazio.")
            return
        
        # Mostrar o pagamento antes de deletar
        pagamento = await self.repo.buscar_por_id(pagamento_id)
        if not pagamento:
            print("❌ Pagamento não encontrado ou ID inválido.")
            return
        
        print(f"\nPagamento a ser deletado:")
        print(f"   {pagamento}")
        
        confirmacao = input("\n⚠️  Tem certeza? Esta ação não pode ser desfeita! (s/N): ").strip().lower()
        
        if confirmacao in ['s', 'sim', 'y', 'yes']:
            sucesso = await self.repo.deletar_por_id(pagamento_id)
            if sucesso:
                print("✅ Pagamento deletado com sucesso!")
            else:
                print("❌ Erro ao deletar pagamento.")
        else:
            print("❌ Operação cancelada.")

    async def mostrar_estatisticas(self):
        print("\n📊 ESTATÍSTICAS DO SISTEMA")
        
        try:
            total = await self.repo.contar_total()
            pendentes = await self.repo.contar_pagamentos_por_status("pendente")
            processados = await self.repo.contar_pagamentos_por_status("processado")
            falharam = await self.repo.contar_pagamentos_por_status("falhou")
            
            print(f"""
┌─────────────────────────────────┐
│         ESTATÍSTICAS            │
├─────────────────────────────────┤
│ Total de pagamentos: {total:>10} │
│ Pendentes:           {pendentes:>10} │
│ Processados:         {processados:>10} │
│ Falharam:            {falharam:>10} │
└─────────────────────────────────┘
            """)
            
            if total > 0:
                print(f"\n📈 Percentuais:")
                print(f"   Pendentes:   {(pendentes/total)*100:.1f}%")
                print(f"   Processados: {(processados/total)*100:.1f}%")
                print(f"   Falharam:    {(falharam/total)*100:.1f}%")
                
        except Exception as e:
            print(f"❌ Erro ao carregar estatísticas: {e}")

    async def executar(self):
        print("🚀 Inicializando sistema...")
        await init()
        print("✅ Conectado ao banco de dados!")
        
        while self.running:
            await self.mostrar_menu()
            
            try:
                opcao = input("\nEscolha uma opção: ").strip()
                
                if opcao == "1":
                    await self.listar_pagamentos_menu()
                elif opcao == "2":
                    await self.buscar_pagamento_menu()
                elif opcao == "3":
                    await self.criar_pagamento_menu()
                elif opcao == "4":
                    await self.atualizar_pagamento_menu()
                elif opcao == "5":
                    await self.deletar_pagamento_menu()
                elif opcao == "6":
                    await self.mostrar_estatisticas()
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
    crud = PagamentoCRUD()
    await crud.executar()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        raise e