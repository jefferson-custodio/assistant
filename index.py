#%%
from ia_model.index import get_answer
from utils import ouvir_microfone, play_audio
from actions import open_work_programs, turn_off

def listen(awake=False):
    message = ouvir_microfone(awake)

    if message != False:
        result, tag, actions = get_answer(message)
        print(result)

        if awake == False and tag == 'greeting':
            play_audio(f'{tag}.mp3')
            awake = True
        else:
            play_audio(f'{tag}.mp3')
            if len(actions) > 0:
                if actions[0] == 'open_work_programs':
                    open_work_programs()
                    awake == False
                elif actions[0] == 'turn_off':
                    turn_off()
                    awake == False
    elif awake == True:
        play_audio('audios/noanswer.mp3')

    return listen(awake)

listen()
# %%
