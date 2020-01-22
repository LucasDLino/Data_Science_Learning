from Introducao_a_Ciencia_de_Dados.Tasks.Simulation import Simulation

def main():
    ### OLHAR
    #sim = Simulation("chuvas_C_00937023.csv") #Estação de Piranhas
    sim = Simulation("stations.txt") # Lista de Estações

    sim.start()

    while(True):
        sim.running()
        #

        answer = str(input("Deseja rodar outra estação ? (S/N)\n"))
        if answer.lower() == "s":
            sim.count_stations += 1
            #file_name = str(input("Digite o nome do arquivo: \n"))
            #sim.new_data(file_name)
            if sim.count_stations > (len(sim.process.stations) - 1):
                print("Não há mais estações para visualizar")
                break
            else:
                pass
        else:
            break

main()
