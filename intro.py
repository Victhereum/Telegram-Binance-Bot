from art import tprint
from logger import logger
from configs import CHANNEL_NAME as channel_name
logo = """                                                                                        
                                       ..............................                               
                                      .::::::::::::::::::::::::::::'                                
                                    .'::::::::::::::::::::::::::::.  .                              
                                   .;:::,.                .,::::,. .                                
                                 .':::;..''''''''',,,,,,,,::::::.                                    
                                .'::;..,:::::::::::::::::::::'.                                     
                                ..... ..''',::::,,,,::::;,;,.                                       
                                           .:::'    ,::;.                                           
                                           .:::'    ;:::.                                           
                                           .;::'   .::::.                                           
                                           .,::..',;::::.                                           
                                           .,::;;::::,..                                            
                                           .';;;;,'..                                               
                                           .','...                                                  
                                           ....    
"""
def introduction():
    logger.info(f'''
    {logo}
    ''')
    tprint("Thamer Bot Initiated")
    print(f"                Awaiting Signal from {channel_name} channel")