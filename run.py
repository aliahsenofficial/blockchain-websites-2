import os
import csv
import subprocess

def airdropalert():
    try:
        subprocess.run(['python', 'airdropalert.py'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running airdropalert.py: {e}")

def airdropbob():
    try:
        subprocess.run(['python', 'airdropbob.py'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running airdropbob.py: {e}")

def airdropking():
    try:
        subprocess.run(['python', 'airdropking.py'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running airdropking.py: {e}")

def airdrops():
    try:
        subprocess.run(['python', 'airdrops.py'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running airdrops.py: {e}")

def galxe():
    try:
        subprocess.run(['python', 'galxe.py'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running galxe.py: {e}")

def giveaway():
    try:
        subprocess.run(['python', 'giveaway.py'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running giveaway.py: {e}")

def guild():
    try:
        subprocess.run(['python', 'guild.py'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running guild.py: {e}")

def questn():
    try:
        subprocess.run(['python', 'questn.py'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running questn.py: {e}")

def taskon():
    try:
        subprocess.run(['python', 'taskon.py'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running taskon.py: {e}")

def zealy():
    try:
        subprocess.run(['python', 'zealy.py'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running zealy.py: {e}")

def alphaquestpro():
    try:
        subprocess.run(['python', 'alphaquestpro.py'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running alphaquestpro.py: {e}")

def alphaquestguest():
    try:
        subprocess.run(['python', 'alphaquestguest.py'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running alphaquestguest.py: {e}")


if __name__ == "__main__":
    # check = input("Alpha Quest Guest or Pro (g/p): ")

    # Checking if Old Scraped.csv file already exists or not
    if os.path.isfile("All_Scraped.csv"):
        print(f">> The file All_Scraped.csv already exists.")
    else:
        with open("All_Scraped.csv", mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Name', 'Report', 'Website', 'Telegram', 'Twitter', 'Discord'])
        print('>> All_Scraped.csv file created.')

    with open("New_Scraped.csv", mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Report', 'Website', 'Telegram', 'Twitter', 'Discord'])
    print('>> New_Scraped.csv file created.\n')

    try:
        print('>> Airdrop Alert Started')
        airdropalert()
        print('>> Airdrop Alert Done\n')
    except:
        print(">> airdropalert.py not working!")

    try:
        print('>> Airdrop Bob Started')
        airdropbob()
        print('>> Airdrop Bob Done\n')
    except:
        print(">> airdropbob.py not working!")
    
    try:
        print('>> Airdrop King Started')
        airdropking()
        print('>> Airdrop King Done\n')
    except:
        print(">> airdropking.py not working!")
    
    try:
        print('>> Airdrops Started')
        airdrops()
        print('>> Airdrops Done\n')
    except:
        print(">> airdrops.py not working!")
    
    try:
        print('>> Giveaway Started')
        giveaway()
        print('>> Giveaway Done\n')
    except:
        print(">> giveaway.py not working!")

    try:
        print('>> Zealy Started')
        zealy()
        print('>> Zealy Done\n')
    except:
        print(">> zealy.py not working!")

    try:
        print('>> TaskOn Started')
        taskon()
        print('>> TaskOn Done\n')
    except:
        print(">> taskon.py not working!")

    try:
        print('>> Galxe Started')
        galxe()
        print('>> Galxe Done\n')
    except:
        print(">> galxe.py not working!")
    
    try:
        print('>> Guild Hall Started')
        guild()
        print('>> Guild Hall Done\n')
    except:
        print(">> guild.py not working!")

    try:
        print('>> QuestN Started')
        questn()
        print('>> QuestN Done\n')
    except:
        print(">> questn.py not working!")

    try:
        print('>> Alpha Quest Guest Started')
        alphaquestguest()
        print('>> Alpha Quest Done\n')
    except:
        print(">> alphaquestguest.py not working!")
        
    # if check.lower() == 'p':
    #     try:
    #         print('>> Alpha Quest Started')
    #         alphaquestpro()
    #         print('>> Alpha Quest Done\n')
    #     except:
    #         print(">> alphaquestpro.py not working!")
    # else:
    #     try:
    #         print('>> Alpha Quest Guest Started')
    #         alphaquestguest()
    #         print('>> Alpha Quest Done\n')
    #     except:
    #         print(">> alphaquestguest.py not working!")
