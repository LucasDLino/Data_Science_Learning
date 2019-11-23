from Introducao_a_Ciencia_de_Dados.Tasks import Simulation

def main():
    sim = Simulation.Simulation()

    sim.start()

    while(True):
        sim.running()
        sim.end()

        answer = str(input("Deseja rodar outra estação ? (S/N)\n"))
        if answer.lower() == "s":
            file_name = str(input("Digite o nome do arquivo: \n"))
            sim.new_data(file_name)
        else:
            break

main()
