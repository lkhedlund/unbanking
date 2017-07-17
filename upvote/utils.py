from django.contrib import messages
from django.core.exceptions import ValidationError

def has_voted(request):
    voted = request.session.get('has_voted', False)
    voted_message = "Thank you for your vote. Be sure to share your word to get the most votes and win!"
    if voted:
        messages.add_message(request, messages.WARNING, voted_message)
        return True
    else:
        return False

def format_word(word):
    lower_word = word.lower()
    if lower_word[-3:] == 'ing':
        return lower_word[:-3]
    else:
        return lower_word

def validate_profanity(word):
    profanity_set = ['bank', 'doggin', 'masochist', 'cumming', 'anal impaler', 'boob', 'cut rope', 'rimming', 'cum guzzler', 'twunter', 'titfuck', 'assfucker', 'hoer', 'fistfuckings', 'need the dick', 'pornos', 'jerk-off', 'shitters', 'labia', 'fuck', 'butt fuck', "bang (one's) box", 'anus', 'kinky Jesus', 'shitted', 'tit', 'hore', 'fuck yo mama', 'muff puff', 't1tties', 'breasts', 'shitfull', 't1tt1e5', 'pissin', 'mothafucked', 'fistfucking', 'niggas', 'fistfucked', 'nigg3r', 'dildos', 'c0cksucker', 'phuq', 'cocksuck', 'niggers', 'fooker', 'knobend', 'jiz', 'felching', 'ballsack', 'god damn', 'knobjocky', 'wtf', 'viagra', 'b00bs', 'flange', 'pube', 'bestiality', 'slut bucket', 'master-bate', 'nut butter', 'phonesex', 'cornhole', 'whore', 'f_u_c_k', 'ma5terb8', 'shited', 'motherfucking', 'cocksucker', 'n1gga', 'm0f0', 'willies', 'hardcoresex', 'a_s_s', 'shitter', 'shitings', 'scrote', 'ham flap', 'mo-fo', 'buttmuch', 'knob', 'ass', 'motherfucker', '5h1t', 'asses', 'cunts', 'b17ch', 'ass fuck', 'fuckings', 'xrated', 'kums', 'cyalis', 'how to kill', 'penis', 'slut', 'skank', 'turd', 'fuckers', 'fucks', 'phuked', 'beef curtain', 'niggah', 'lmao', 'vagina', 'beastial', 'm45terbate', 'cuntlicking', 'fannyfucker', 's.o.b.', 'fingerfuck', 'blowjobs', 'ass-fucker', 'feck', 'cunnilingus', 'twat', 'bitch', 'm0fo', 'pigfucker', 'kondum', 'cummer', 'motherfucks', 'sadist', 'bunny fucker', 'goddamn', 'cock pocket', 'fuck-bitch', 'v14gra', 'cyberfuc', 'cuntlick', 'pecker', 'dick hole', 'chink', 'clitoris', 'twathead', 'eat hair pie', 'fuckme', 'nobhead', 'fuckin', 'corp whore', 'cums', 'fuks', 'fuckheads', 'lmfao', 'phukked', 'f u c k', 'shagger', 'shemale', 'fistfucker', 'pussies', 'dyke', 'doggie style', 'amateur', 'choade', 's hit', 'fellate', 'orgasims', 'clit licker', 'pissflaps', 'twunt', 'bust a load', 'chota bags', 'fatass', 'anilingus', 'ejaculate', 'omg', 'fuk', 'fuck trophy', 'assholes', 'phuk', 'fcuking', 'blow me', 'cocksucking', 'motherfuckin', 'fagging', 'cawk', 'mutherfucker', 'tittie5', 'ejaculation', 'dinks', 'homo', 'shitey', 'god', 'pusse', 'vulva', 'bitcher', 'f u c k e r', 'queer', 'LEN', 'fistfucks', 'gaylord', 'knobhead', 'fuck-ass', 'nob jokey', 'v1gra', 'scrotum', 'beastiality', 'mother fucker', 'fudge packer', 'dickhead', 'titties', 'butt', 'jackoff', 'b!tch', 'shagging', 'bi+ch', '50 yard cunt punt', 'fags', 'eat a dick', 'bitches', 'porno', 'cuntlicker', 'pawn', 'phuks', 'sh!+', 'kum', 'spunk', 'tw4t', 'fcuk', 'bollok', 'cockface', 'knobead', 'shaggin', 'bellend', 'ejaculatings', 'dogging', 'shitfuck', 'booooooobs', 'nigger', 'c0ck', 'schlong', 'ballbag', 'cyberfucker', 'fanyy', 'pissers', 'busty', 'son-of-a-bitch', 'bloody', 'mothafuckaz', 'masterbat*', 'fux', 'faggot', 'scroat', 'nobjocky', 'teets', 'fucktoy', 'shit fucker', 'hoar', 'cunillingus', 'fanny', 'snatch', 'l3i+ch', 'pissoff', 'jap', 'rimjaw', 'mof0', 'wanker', 'fingerfucked', 'tittywank', 'fukkin', 'dirty Sanchez', 'masterbate', 'shitting', '4r5e', 'masturbate', 'kummer', 'mothafucking', 'clusterfuck', 'nutsack', 'p0rn', 'smegma', 'pissing', 'hotsex', 'bastard', 'duche', 'hell', 'teez', 'mothafucks', 'damn', 'flog the log', 'lusting', 'fingerfucking', 'cum chugger', 'shits', 'titt', 'cock snot', 'cop some wood', 'erotic', 'cum', 'pornography', 'cocksucked', 'nigga', 'dlck', 'tit wank', 'phuking', 'kock', 'bugger', 'f4nny', 'motherfuckings', 'buceta', 'pron', 'porn', 'ejaculating', 'shag', 'masterb8', 'faggitt', 'carpet muncher', 'kwif', 'bareback', 'mothafuck', 'sandbar', 'cumshot', 'bollock', 'smut', 'pimpis', 'mothafuckers', 'd1ck', 'fukwhit', 'shite', 'fudgepacker', 'cunilingus', 'cunt-struck', 'faggs', 'gangbanged', 'wank', 'blow job', 'phukking', 'jism', 'jack-off', 'coon', 'birdlock', 'a55', 'slope', 'cok', 'xxx', 'poop', 'niggaz', 'clitty litter', 'pissed', 'gangbang', 'horny', 'tosser', '5hit', 'orgasms', 'jizm', 'wanky', 'assmucus', 'fux0r', 'fucker', 'fuck puppet', 'blue waffle', 'booobs', 'cox', 'cumdump', 'fannyflaps', 'mothafuckings', 'nazi', 'clits', 'willy', 'adult', 'nobjokey', 'buttplug', 'clit', 'screwing', 'asshole', 'fucking', 'shitdick', 'goddamned', 'tittyfuck', 'donkeyribber', 'knobed', 'blumpkin', 'shithead', 'cocksucks', 'ejaculates', 'fukwit', 'bitch tit', 'cock', 'pussys', 'spac', 'fuckingshitmotherfucker', 'cockmuncher', 'mothafucker', 'fistfuck', 'shittings', 'ejaculated', 'bitchers', 'assmunch', 'kumming', 'masterbation', 'motherfucked', 'doosh', 'boobs', 'fist fuck', 'cnut', 'facial', 'fingerfucks', 'fuker', 'testicle', 'cokmuncher', 'retard', 'blow mud', 'penisfucker', 'boiolas', 'goatse', 'semen', 'ar5e', 'cum freak', 'gang-bang', 'jizz', 'dick shy', 'mofo', 'bestial', 'booooobs', 'mafugly', 'bitching', 'phuck', 'arse', 'cockhead', 'kunilingus', 'knob end', 'cyberfuckers', 'anal leakage', 'cocksuka', 'cunt hair', 'fuckmeat', 'l3itch', 'sluts', 'nigg4h', 'pisser', 'cyberfuck', 'bangbros', 'fellatio', 'dirsa', 'cocks', 'fuckwit', 'knobjokey', 'fag', 'dick', 'fcuker', 'muthafuckker', 'piss', 'cipa', 'homoerotic', 'arrse', 'how to murdep', 'cuntbag', 'cockmunch', 'b1tch', 'hoare', 'motherfuck', 'numbnuts', 'mothafuckin', 'cyberfucking', 'cl1t', 'dildo', 'boner', 'queaf', 'shiting', 'pussi', 'assfukka', 'gassy ass', 'mutha', 'fuck hole', 'cocksukka', 'muther', 'pussy palace', 'kondums', 'pisses', 'fecker', 'fuckwhit', 'bitchin', 'bum', 'masterbations', 'motherfuckers', 'fuckhead', 'pussy', 's_h_i_t', 'cunt', 'bimbos', 'asswhole', 'sausage queen', 'w00se', 'sex', 'shi+', 'shitty', 'coksucka', 'arsehole', 'nob', 'n1gger', 'butthole', 'masterbat3', 'fagot', 'horniest', 'tittiefucker', 'fukker', 'cuntsicle', 'god-dam', 'heshe', 'fook', 'tits', 'fistfuckers', 'cock-sucker', 'fucka', 'fingerfuckers', 'kawk', 'mothafuckas', 'fucked', 'jerk', 'ejakulate', 'testical', 'a2m', 'muff', 'mothafucka', 'fagots', 'god-damned', 'sh!t', 'lust', 'twatty', 'gaysex', 'doggiestyle', 'rectum', 'sh1t', 'blowjob', 'orgasm', 'ma5terbate', 'dog-fucker', 'fingerfucker', 'anal', 'orgasim', 'titwank', 'boooobs', 'autoerotic', 'biatch', 'sadism', 'prick', 'wang', 'muthafecker', 'pussy fart', 'shit', 'motherfuckka', 'whoar', 'cyberfucked', 'dink', 'carpetmuncher', 'cum dumpster', 'pricks', 'gangbangs']

    lower_word = word.lower()

    if lower_word in profanity_set:
        raise ValidationError("Let's keep this classy, please.")
    for swear in profanity_set:
        if swear in lower_word:
            raise ValidationError("Let's keep this classy, please.")