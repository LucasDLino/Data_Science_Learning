from Introd_a_Ciencia_de_Dados.Tasks.Simulation import Simulation

def main():
    sim = Simulation("stations.txt") # Lista de Estações

    sim.start()

    while(True):
        sim.running()

        answer = str(input("Deseja rodar outra estação ? (S/N)\n"))
        if answer.lower() == "s":
            sim.count_stations += 1

            if sim.count_stations > (len(sim.process.stations) - 1):
                print("Não há mais estações para visualizar")
                break
            else:
                pass
        else:
            if answer.lower() == "n":
                print("Programa finalizado")
                break
            else:
                print("Opção inválida ... encerrando o programa")
                break

main()
