#!/usr/bin/env python3
import os
import sqlite3
import sys
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

DB_PATH = 'data/prayers.db'
SCHEMA_PATH = 'schema.sql'

PRAYERS = [
    # Ave Maria
    {
        'key': 'hail_mary',
        'category': 'rosary',
        'title': 'Ave Maria',
        'text': {
            'it': 'Ave Maria, piena di grazia, il Signore è con te. Tu sei benedetta fra le donne e benedetto è il frutto del tuo seno, Gesù. Santa Maria, Madre di Dio, prega per noi peccatori, adesso e nell\'ora della nostra morte. Amen.',
            'en': 'Hail Mary, full of grace. The Lord is with thee. Blessed art thou amongst women and blessed is the fruit of thy womb, Jesus. Holy Mary, Mother of God, pray for us sinners, now and at the hour of our death. Amen.',
            'es': 'Dios te salve, María, llena eres de gracia; el Señor es contigo. Bendita tú eres entre todas las mujeres y bendito es el fruto de tu vientre, Jesús. Santa María, Madre de Dios, ruega por nosotros pecadores, ahora y en la hora de nuestra muerte. Amén.',
            'pt': 'Ave Maria cheia de graça, o Senhor é convosco; bendita sois vós entre as mulheres e bendito é o fruto do vosso ventre, Jesus. Santa Maria, Mãe de Deus, rogai por nós, pecadores, agora e na hora de nossa morte. Amém.'
        }
    },
    # Padre Nostro
    {
        'key': 'our_father',
        'category': 'daily',
        'title': 'Padre Nostro',
        'text': {
            'it': 'Padre nostro che sei nei cieli, sia santificato il tuo nome, venga il tuo regno, sia fatta la tua volontà, come in cielo così in terra. Dacci oggi il nostro pane quotidiano, e rimetti a noi i nostri debiti come noi li rimettiamo ai nostri debitori, e non ci indurre in tentazione, ma liberaci dal male. Amen.',
            'en': 'Our Father, who art in heaven, hallowed be thy name. Thy kingdom come, thy will be done, on earth as it is in heaven. Give us this day our daily bread; and forgive us our trespasses as we forgive those who trespass against us; and lead us not into temptation, but deliver us from evil. Amen.',
            'es': 'Padre nuestro que estás en los cielos, santificado sea tu nombre; venga tu reino; hágase tu voluntad, así en la tierra como en el cielo. Danos hoy nuestro pan de cada día; y perdona nuestras ofensas así como nosotros perdonamos a los que nos ofenden; no nos dejes caer en la tentación y líbranos del mal. Amén.',
            'pt': 'Pai nosso, que estais no céu, santificado seja o vosso nome; venha a nós o vosso reino; seja feita a vossa vontade, assim na terra como no céu. O pão nosso de cada dia nos dai hoje; perdoai-nos as nossas ofensas, assim como nós perdoamos a quem nos tem ofendido; e não nos deixeis cair em tentação, mas livrai-nos do mal. Amém.'
        }
    },
    # Gloria al Padre
    {
        'key': 'glory_be',
        'category': 'daily',
        'title': 'Gloria al Padre',
        'text': {
            'it': 'Gloria al Padre, al Figlio e allo Spirito Santo. Come era nel principio, ora e sempre nei secoli dei secoli. Amen.',
            'en': 'Glory be to the Father, and to the Son, and to the Holy Spirit. As it was in the beginning, is now, and ever shall be, world without end. Amen.',
            'es': 'Gloria al Padre, y al Hijo, y al Espíritu Santo. Como era en el principio, ahora y siempre, por los siglos de los siglos. Amén.',
            'pt': 'Glória ao Pai, ao Filho e ao Espírito Santo. Como era no princípio, agora e sempre, e nos séculos dos séculos. Amém.'
        }
    },
    # Credo degli Apostoli
    {
        'key': 'apostles_creed',
        'category': 'daily',
        'title': 'Credo degli Apostoli',
        'text': {
            'it': 'Credo in Dio, Padre onnipotente, Creatore del cielo e della terra. E in Gesù Cristo, suo unico Figlio, nostro Signore ... Amen.',
            'en': 'I believe in God, the Father almighty, Creator of heaven and earth. And in Jesus Christ, his only Son, our Lord ... Amen.',
            'es': 'Creo en Dios Padre todopoderoso, Creador del cielo y de la tierra. Y en Jesucristo, su único Hijo, Nuestro Señor ... Amén.',
            'pt': 'Creio em Deus Pai todo-poderoso, Criador do céu e da terra. E em Jesus Cristo, seu único Filho, Nosso Senhor ... Amém.'
        }
    },
    # Angelus
    {
        'key': 'angelus',
        'category': 'marian',
        'title': 'Angelus',
        'text': {
            'it': 'L: L’angelo del Signore portò l’annunzio a Maria. R: Ed ella concepì per opera dello Spirito Santo. ...',
            'en': 'V. The angel of the Lord declared unto Mary. R. And she conceived by the Holy Spirit. ...',
            'es': 'V. El ángel del Señor anunció a María. R. Y concibió por obra del Espíritu Santo. ...',
            'pt': 'V. O anjo do Senhor anunciou a Maria. R. E ela concebeu do Espírito Santo. ...'
        }
    },
    # Regina Coeli (pasquale)
    {
        'key': 'regina_coeli',
        'category': 'marian',
        'title': 'Regina Coeli',
        'text': {
            'it': 'Regina coeli, laetare, alleluia. Quia quem meruisti portare, alleluia, resurrexit sicut dixit, alleluia ...',
            'en': 'Queen of Heaven, rejoice, alleluia. For He whom thou didst merit to bear, alleluia, has risen as he said, alleluia ...',
            'es': 'Regina coeli, laetare, alleluia. Quia quem meruisti portare, alleluia, resurrexit sicut dixit, alleluia ...',
            'pt': 'Regina caeli, laetare, alleluia. Quia quem meruisti portare, alleluia, resurrexit sicut dixit, alleluia ...'
        }
    },
    # Atto di dolore
    {
        'key': 'act_of_contrition',
        'category': 'daily',
        'title': 'Atto di dolore',
        'text': {
            'it': 'O mio Dio, mi pento e mi dolgo di tutto cuore dei miei peccati…',
            'en': 'O my God, I am heartily sorry for having offended Thee, and I detest all my sins...',
            'es': 'Dios mío, me arrepiento de todo corazón de haberte ofendido...',
            'pt': 'Ó meu Deus, arrependo-me de todo o coração de Vos ter ofendido...'
        }
    },
    # Preghiera di San Francesco
    {
        'key': 'prayer_of_saint_francis',
        'category': 'daily',
        'title': 'Preghiera di San Francesco',
        'text': {
            'it': 'Signore, fa\' di me uno strumento della tua pace. Dove è odio, ch\'io porti l\'amore; dove è offesa, ch\'io porti il perdono; dove è discordia, ch\'io porti l\'unione; dove è dubbio, ch\'io porti la fede; dove è errore, ch\'io porti la verità; dove è disperazione, ch\'io porti la speranza; dove è tristezza, ch\'io porti la gioia; dove sono le tenebre, ch\'io porti la luce. Maestro, fa\' che io non cerchi tanto: essere consolato, quanto consolare; essere compreso, quanto comprendere; essere amato, quanto amare. Poiché è dando, che si riceve; è perdonando, che si è perdonati; è morendo, che si risuscita a vita eterna. Amen.',
            'en': 'Lord, make me an instrument of your peace. Where there is hatred, let me sow love; where there is injury, pardon; where there is discord, union; where there is doubt, faith; where there is error, truth; where there is despair, hope; where there is sadness, joy; where there are shadows, light. O Divine Master, grant that I may not so much seek to be consoled, as to console; to be understood, as to understand; to be loved, as to love. For it is in giving that we receive; it is in pardoning that we are pardoned; and it is in dying that we are born to eternal life. Amen.',
            'es': 'Señor, haz de mí un instrumento de tu paz. Donde haya odio, que yo ponga amor; donde haya ofensa, que yo ponga perdón; donde haya discordia, que yo ponga unión; donde haya duda, que yo ponga fe; donde haya error, que yo ponga verdad; donde haya desesperación, que yo ponga esperanza; donde haya tristeza, que yo ponga alegría; donde haya tinieblas, que yo ponga luz. Maestro, concédeme que yo no busque tanto: ser consolado, como consolar; ser comprendido, como comprender; ser amado, como amar. Porque es dando como se recibe; es perdonando como se es perdonado; y es muriendo como se resucita a la vida eterna. Amén.',
            'pt': 'Senhor, fazei de mim um instrumento da vossa paz. Onde houver ódio, que eu leve o amor; onde houver ofensa, que eu leve o perdão; onde houver discórdia, que eu leve a união; onde houver dúvida, que eu leve a fé; onde houver erro, que eu leve a verdade; onde houver desespero, que eu leve a esperança; onde houver tristeza, que eu leve a alegria; onde houver trevas, que eu leve a luz. Mestre, fazei que eu procure menos: ser consolado do que consolar; ser compreendido do que compreender; ser amado do que amar. Pois é dando que se recebe; é perdoando que se é perdoado; e é morrendo que se ressuscita para a vida eterna. Amém.'
        }
    },
    # Coroncina della Divina Misericordia
    {
        'key': 'divine_mercy_chaplet',
        'category': 'daily',
        'title': 'Coroncina della Divina Misericordia',
        'text': {
            'it': 'Eterno Padre, offro a te il Corpo e il Sangue, l\'Anima e la Divinità del tuo amatissimo Figlio, Nostro Signore Gesù Cristo, in espiazione dei nostri peccati e di quelli del mondo intero. (Si recita sui grani del Padre Nostro.) Per la sua dolorosa Passione, abbi misericordia di noi e del mondo intero. (Si recita sui 10 grani dell\'Ave Maria.) Santo Dio, Santo Forte, Santo Immortale, abbi pietà di noi e del mondo intero. (Si recita 3 volte alla fine.) Amen.',
            'en': 'Eternal Father, I offer you the Body and Blood, Soul and Divinity of Your dearly beloved Son, Our Lord Jesus Christ, in atonement for our sins and those of the whole world. (On the Our Father beads.) For the sake of His sorrowful Passion, have mercy on us and on the whole world. (On the Hail Mary beads, 10 times.) Holy God, Holy Mighty One, Holy Immortal One, have mercy on us and on the whole world. (Three times at the end.) Amen.',
            'es': 'Padre Eterno, te ofrezco el Cuerpo y la Sangre, el Alma y la Divinidad de tu amadísimo Hijo, Nuestro Señor Jesucristo, en expiación de nuestros pecados y los del mundo entero. (En los granos del Padre Nuestro.) Por su dolorosa Pasión, ten misericordia de nosotros y del mundo entero. (En los 10 granos del Ave María.) Santo Dios, Santo Fuerte, Santo Inmortal, ten piedad de nosotros y del mundo entero. (Tres veces al final.) Amén.',
            'pt': 'Pai Eterno, ofereço-vos o Corpo e o Sangue, a Alma e a Divindade do vosso amado Filho, Nosso Senhor Jesus Cristo, em reparação dos nossos pecados e dos do mundo inteiro. (Nos grãos do Pai Nosso.) Pela sua dolorosa Paixão, tende misericórdia de nós e do mundo inteiro. (Nos 10 grãos da Ave-Maria.) Santo Deus, Santo Forte, Santo Imortal, tende piedade de nós e do mundo inteiro. (Três vezes no final.) Amém.'
        }
    },
    # Preghiera del mattino
    {
        'key': 'morning_prayer',
        'category': 'daily',
        'title': 'Preghiera del mattino',
        'text': {
            'it': 'Dio onnipotente ed eterno, ti ringrazio di cuore per aver vegliato su di me questa notte e per avermi concesso di vedere questo nuovo giorno. Ti offro tutto ciò che farò oggi: i miei pensieri, le mie parole, le mie azioni, le mie gioie e le mie sofferenze. Fa\' che tutto ciò che farò oggi sia per la tua gloria e per il bene delle anime. Guidami in questo giorno, preservami dal peccato e da ogni male. Amen.',
            'en': 'Almighty and eternal God, I thank you heartily for watching over me this night and for granting me to see this new day. I offer you all that I will do today: my thoughts, my words, my actions, my joys and my sufferings. May all I do today be for your glory and for the good of souls. Guide me through this day, preserve me from sin and from all evil. Amen.',
            'es': 'Dios todopoderoso y eterno, te doy gracias de corazón por haber velado sobre mí esta noche y por haberme concedido ver este nuevo día. Te ofrezco todo lo que haré hoy: mis pensamientos, mis palabras, mis acciones, mis alegrías y mis sufrimientos. Haz que todo lo que haga hoy sea para tu gloria y el bien de las almas. Guíame en este día, presérvame del pecado y de todo mal. Amén.',
            'pt': 'Deus todo-poderoso e eterno, agradeço-te de coração por teres velado sobre mim esta noite e por me teres concedido ver este novo dia. Ofereço-te tudo o que farei hoje: os meus pensamentos, as minhas palavras, as minhas ações, as minhas alegrias e os meus sofrimentos. Faz que tudo o que eu fizer hoje seja para a tua glória e o bem das almas. Guia-me neste dia, preserva-me do pecado e de todo mal. Amém.'
        }
    },
    # Preghiera della sera
    {
        'key': 'evening_prayer',
        'category': 'daily',
        'title': 'Preghiera della sera',
        'text': {
            'it': 'O Signore Dio, ti ringrazio per questo giorno che volge al termine. Hai vegliato su di me durante le ore di lavoro e di riposo. Ti chiedo perdono per ogni mancanza commessa oggi. Purifica il mio cuore durante questa notte e preservami da ogni pericolo. Affido a te la mia anima, il mio corpo, la mia famiglia e tutti coloro che mi sono cari. Amen.',
            'en': 'O Lord God, I thank you for this day that is drawing to a close. You have watched over me during the hours of work and rest. I ask your forgiveness for every fault committed today. Purify my heart during this night and preserve me from all danger. I entrust to you my soul, my body, my family, and all those dear to me. Amen.',
            'es': 'Oh Señor Dios, te doy gracias por este día que llega a su fin. Has velado sobre mí durante las horas de trabajo y descanso. Te pido perdón por cada falta cometida hoy. Purifica mi corazón durante esta noche y presérvame de todo peligro. Te encomiendo mi alma, mi cuerpo, mi familia y todos los que me son queridos. Amén.',
            'pt': 'Ó Senhor Deus, agradeço-te por este dia que chega ao fim. Velaste sobre mim durante as horas de trabalho e descanso. Peço-te perdão por cada falta cometida hoje. Purifica o meu coração durante esta noite e preserva-me de todo perigo. Confio-te a minha alma, o meu corpo, a minha família e todos os que me são queridos. Amém.'
        }
    },
    # Preghiera per i defunti
    {
        'key': 'prayer_for_the_dead',
        'category': 'daily',
        'title': 'Preghiera per i defunti',
        'text': {
            'it': 'O Signore, dona la pace eterna alle anime dei fedeli defunti, specialmente a coloro che mi sono stati cari. La luce perpetua risplenda su di loro. Riposino in pace. Amen.',
            'en': 'O Lord, grant eternal rest to the souls of the faithful departed, especially those who were dear to me. May perpetual light shine upon them. May they rest in peace. Amen.',
            'es': 'Oh Señor, concede el eterno descanso a las almas de los fieles difuntos, especialmente a los que me fueron queridos. La luz perpetua brille sobre ellos. Descansen en paz. Amén.',
            'pt': 'Ó Senhor, concede o descanso eterno às almas dos fiéis defuntos, especialmente àqueles que me foram queridos. A luz perpétua brilhe sobre eles. Descansem em paz. Amém.'
        }
    },
    # Preghiera per i malati
    {
        'key': 'prayer_for_the_sick',
        'category': 'daily',
        'title': 'Preghiera per i malati',
        'text': {
            'it': 'O Gesù, che hai guarito tanti malati durante la tua vita terrena, guarda con misericordia tutti i malati del mondo. Allevia le loro sofferenze, dona loro la speranza, e se è nella tua volontà, restituiscili alla salute. Sostieni le loro famiglie e chi si prende cura di loro. Amen.',
            'en': 'O Jesus, who healed so many sick during your earthly life, look with mercy upon all the sick in the world. Alleviate their sufferings, give them hope, and if it is your will, restore them to health. Support their families and those who care for them. Amen.',
            'es': 'Oh Jesús, que sanaste a tantos enfermos durante tu vida terrena, mira con misericordia a todos los enfermos del mundo. Alivia sus sufrimientos, dales esperanza y, si es tu voluntad, devuélvelos a la salud. Sostén a sus familias y a quienes cuidan de ellos. Amén.',
            'pt': 'Ó Jesus, que curaste tantos doentes durante a tua vida terrena, olha com misericórdia para todos os doentes do mundo. Alivia os seus sofrimentos, dá-lhes esperança e, se for a tua vontade, restitui-lhes a saúde. Sustenta as suas famílias e quem cuida deles. Amém.'
        }
    },
    # Preghiera prima della Confessione
    {
        'key': 'prayer_before_confession',
        'category': 'sacraments',
        'title': 'Preghiera prima della Confessione',
        'text': {
            'it': 'O Spirito Santo, illumina la mia mente e il mio cuore perché possa vedere chiaramente i miei peccati. Donami un sincero dolore per averli commessi e il fermo proposito di non ricadervi. Maria, Madre di misericordia, intercedi per me. Amen.',
            'en': 'O Holy Spirit, enlighten my mind and heart so that I may see my sins clearly. Grant me sincere sorrow for having committed them and a firm purpose not to fall into them again. Mary, Mother of mercy, intercede for me. Amen.',
            'es': 'Oh Espíritu Santo, ilumina mi mente y mi corazón para que pueda ver claramente mis pecados. Concédeme un sincero dolor por haberlos cometido y el firme propósito de no reincidir en ellos. María, Madre de misericordia, intercede por mí. Amén.',
            'pt': 'Ó Espírito Santo, ilumina a minha mente e o meu coração para que possa ver claramente os meus pecados. Concede-me um sincero arrependimento por os ter cometido e o firme propósito de não reincidir neles. Maria, Mãe de misericórdia, intercede por mim. Amém.'
        }
    },
    # Preghiera di ringraziamento dopo la Comunione
    {
        'key': 'prayer_after_communion',
        'category': 'sacraments',
        'title': 'Preghiera di ringraziamento dopo la Comunione',
        'text': {
            'it': 'O Gesù, sei venuto a me! Ti accolgo con tutto il mio cuore. Rimani con me, non lasciarmi. Trasforma la mia vita con la tua presenza. Fa\' che io ti porti agli altri con la mia vita. Grazie, Signore, per questo dono immenso. Amen.',
            'en': 'O Jesus, you have come to me! I welcome you with all my heart. Remain with me, do not leave me. Transform my life with your presence. May I bring you to others through my life. Thank you, Lord, for this immense gift. Amen.',
            'es': 'Oh Jesús, ¡has venido a mí! Te acojo con todo mi corazón. Permanece conmigo, no me dejes. Transforma mi vida con tu presencia. Haz que te lleve a los demás con mi vida. Gracias, Señor, por este inmenso don. Amén.',
            'pt': 'Ó Jesus, vieste a mim! Acolho-te com todo o meu coração. Fica comigo, não me abandones. Transforma a minha vida com a tua presença. Faz que eu te leve aos outros com a minha vida. Obrigado, Senhor, por este imenso dom. Amém.'
        }
    },
    # Memorare
    {
        'key': 'memorare',
        'category': 'marian',
        'title': 'Memorare',
        'text': {
            'it': 'Ricordati, o piissima Vergine Maria, che non si è mai udito al mondo che alcuno abbia ricorso al tuo patrocinio, implorato il tuo aiuto, chiesto la tua intercessione e sia stato abbandonato. Animato da tale fiducia, a te ricorro, o Vergine delle Vergini e Madre mia; a te vengo, davanti a te mi prostro peccatore pentito. O Madre del Verbo incarnato, non disprezzare le mie suppliche, ma ascoltale propizia ed esaudiscile. Amen.',
            'en': 'Remember, O most gracious Virgin Mary, that never was it known that anyone who fled to thy protection, implored thy help, or sought thine intercession was left unaided. Inspired by this confidence, I fly unto thee, O Virgin of virgins, my Mother; to thee do I come, before thee I stand, sinful and sorrowful. O Mother of the Word Incarnate, despise not my petitions, but in thy mercy hear and answer me. Amen.',
            'es': 'Acuérdate, oh piadosísima Virgen María, que jamás se ha oído decir que ninguno de los que han acudido a tu protección, implorado tu auxilio y reclamado tu socorro haya sido abandonado. Animado por esta confianza, a ti acudo, oh Madre, Virgen de las vírgenes; a ti vengo, ante ti me presento gemebundo y pecador. No quieras, oh Madre del Verbo Encarnado, desechar mis súplicas, antes bien, escúchalas y acógelas benignamente. Amén.',
            'pt': 'Lembrai-vos, ó dulcíssima Virgem Maria, que jamais se ouviu dizer que algum daqueles que recorreram ao vosso patrocínio, imploraram o vosso auxílio ou buscaram o vosso socorro tenha sido abandonado. Animado por esta confiança, a vós recorro, ó Mãe, Virgem das Virgens; a vós venho, diante de vós me apresento, pecador e gemendo. Não desprezeis as minhas súplicas, ó Mãe do Verbo Encarnado, mas atendei-as e ouvi-as propiciamente. Amém.'
        }
    },
    # Inno Te Deum
    {
        'key': 'te_deum',
        'category': 'hymn',
        'title': 'Te Deum',
        'text': {
            'it': 'Noi ti lodiamo, o Dio, noi ti proclamiamo Signore. O eterno Padre, tutta la terra ti adora. A te cantano gli angeli e tutte le potenze dei cieli: Santo, Santo, Santo il Signore Dio dell\'universo. I cieli e la terra sono pieni della tua gloria. Ti proclama il glorioso coro degli apostoli, ti loda la schiera ammirabile dei profeti, ti esalta l\'esercito candido dei martiri. La santa Chiesa in tutto il mondo proclama la tua gloria: Padre di maestà infinita, il tuo venerando vero e unico Figlio, e lo Spirito Santo Paraclito. Tu sei il re della gloria, o Cristo, tu sei il Figlio eterno del Padre. Amen.',
            'en': 'We praise thee, O God; we acknowledge thee to be the Lord. All the earth doth worship thee, the Father everlasting. To thee all angels cry aloud, the heavens and all the powers therein. To thee cherubim and seraphim continually do cry: Holy, Holy, Holy, Lord God of Sabaoth. Heaven and earth are full of the majesty of thy glory. The glorious company of the apostles praise thee. The goodly fellowship of the prophets praise thee. The noble army of martyrs praise thee. The holy Church throughout all the world doth acknowledge thee. Amen.',
            'es': 'A ti, oh Dios, te alabamos; a ti, Señor, te reconocemos. A ti, Padre eterno, te venera toda la creación. Los ángeles todos, los cielos y todas las potestades te honran. Los querubines y serafines te cantan sin cesar: Santo, Santo, Santo es el Señor Dios de los ejércitos. Los cielos y la tierra están llenos de la majestad de tu gloria. A ti te ensalza el glorioso coro de los apóstoles. Amén.',
            'pt': 'A ti, ó Deus, louvamos; a ti, Senhor, reconhecemos. A ti, Pai eterno, toda a terra venera. A ti todos os anjos, os céus e todas as potestades te aclamam. A ti os querubins e serafins com voz incessante proclamam: Santo, Santo, Santo é o Senhor Deus dos exércitos. Os céus e a terra estão cheios da majestade da tua glória. A ti glorifica o admirável coro dos apóstolos. Amém.'
        }
    },
    # Esame di coscienza
    {
        'key': 'examination_of_conscience',
        'category': 'sacraments',
        'title': 'Esame di coscienza',
        'text': {
            'it': 'Prima di ricevere il sacramento della Riconciliazione, prenditi un momento di silenzio e rifletti:\n\n— Ho messo Dio al primo posto nella mia vita, o ho dato troppa importanza ad altre cose?\n— Ho pregato ogni giorno? Ho partecipato alla Messa domenicale?\n— Ho usato il nome di Dio o dei santi in modo irrispettoso?\n— Ho onorato e rispettato i miei genitori e chi ha autorità su di me?\n— Ho rispettato la vita propria e altrui, con le parole e con i fatti?\n— Sono stato onesto? Ho rubato, imbrogliato o detto menzogne?\n— Ho rispettato la dignità degli altri nelle mie parole, sguardi e azioni?\n— Ho preso ciò che non mi apparteneva, o ho danneggiato i beni altrui?\n— Ho detto false testimonianze o diffuso maldicenze su altri?\n— Ho provato invidia o desiderato ciò che appartiene al prossimo?\n\nPoi recita un atto di dolore sincero e confida nella misericordia di Dio.',
            'en': 'Before receiving the sacrament of Reconciliation, take a moment of silence and reflect:\n\n— Have I put God first in my life, or have I given too much importance to other things?\n— Have I prayed every day? Have I attended Sunday Mass?\n— Have I used the name of God or the saints disrespectfully?\n— Have I honored and respected my parents and those in authority over me?\n— Have I respected the life of myself and others, in words and deeds?\n— Have I been honest? Have I stolen, cheated, or told lies?\n— Have I respected the dignity of others in my words, looks, and actions?\n— Have I taken what did not belong to me, or damaged the property of others?\n— Have I given false testimony or spread gossip about others?\n— Have I felt envy or desired what belongs to my neighbor?\n\nThen recite a sincere act of contrition and trust in God\'s mercy.',
            'es': 'Antes de recibir el sacramento de la Reconciliación, tómate un momento de silencio y reflexiona:\n\n— ¿He puesto a Dios en primer lugar en mi vida, o he dado demasiada importancia a otras cosas?\n— ¿He rezado cada día? ¿He asistido a la Misa del domingo?\n— ¿He usado el nombre de Dios o de los santos de manera irrespetuosa?\n— ¿He honrado y respetado a mis padres y a quienes tienen autoridad sobre mí?\n— ¿He respetado la vida propia y ajena, con palabras y con hechos?\n— ¿He sido honesto? ¿He robado, engañado o dicho mentiras?\n— ¿He respetado la dignidad de los demás en mis palabras, miradas y acciones?\n— ¿He tomado lo que no me pertenecía, o he dañado los bienes ajenos?\n— ¿He dado falso testimonio o difundido calumnias sobre otros?\n— ¿He sentido envidia o deseado lo que pertenece a mi prójimo?\n\nLuego recita un sincero acto de contrición y confía en la misericordia de Dios.',
            'pt': 'Antes de receber o sacramento da Reconciliação, reserve um momento de silêncio e reflita:\n\n— Coloquei Deus em primeiro lugar na minha vida, ou dei muita importância a outras coisas?\n— Rezei todos os dias? Participei da Missa dominical?\n— Usei o nome de Deus ou dos santos de forma desrespeitosa?\n— Honrei e respeitei meus pais e aqueles que têm autoridade sobre mim?\n— Respeitei a vida própria e alheia, com palavras e ações?\n— Fui honesto? Roubei, enganei ou disse mentiras?\n— Respeitei a dignidade dos outros em minhas palavras, olhares e ações?\n— Tomei o que não me pertencia ou danifiquei os bens alheios?\n— Dei falso testemunho ou espalhei calúnias sobre outros?\n— Senti inveja ou desejei o que pertence ao meu próximo?\n\nEm seguida, recite um sincero ato de contrição e confie na misericórdia de Deus.'
        }
    },
]

MYSTERY_DEFS = {
    'joyful': [
        (1, 'Annunciazione al Padre', 'Lc 1,26-38', 'monday,saturday'),
        (2, 'Visitazione di Maria a Elisabetta', 'Lc 1,39-56', 'tuesday,saturday'),
        (3, 'Nascita di Gesù a Betlemme', 'Lc 2,1-20', 'wednesday,saturday'),
        (4, 'Presentazione al Tempio', 'Lc 2,22-38', 'thursday,saturday'),
        (5, 'Gesù ritrovato nel Tempio', 'Lc 2,41-52', 'friday,saturday'),
    ],
    'sorrowful': [
        (1, 'Agonia nell\'orto', 'Mt 26,36-46', 'tuesday,friday'),
        (2, 'Flagellazione', 'Gv 19,1', 'tuesday,friday'),
        (3, 'Incoronazione di spine', 'Mt 27,27-31', 'tuesday,friday'),
        (4, 'Porta della croce', 'Gv 19,17', 'tuesday,friday'),
        (5, 'Crocifissione e morte', 'Gv 19,18-30', 'tuesday,friday'),
    ],
    'glorious': [
        (1, 'Resurrezione di Gesù', 'Mt 28,1-10', 'sunday,wednesday'),
        (2, 'Ascensione', 'At 1,6-11', 'thursday'),
        (3, 'Discesa dello Spirito Santo', 'At 2,1-4', 'sunday'),
        (4, 'Assunzione di Maria', 'Ap 12,1-2', 'monday'),
        (5, 'Coronazione di Maria', 'Ap 12,1-5', 'tuesday'),
    ],
    'luminous': [
        (1, 'Battesimo di Gesù', 'Mt 3,13-17', 'thursday'),
        (2, 'Nozze di Cana', 'Gv 2,1-12', 'friday'),
        (3, 'Proclamazione del Regno', 'Mc 1,14-15', 'wednesday'),
        (4, 'Trasfigurazione', 'Mt 17,1-9', 'thursday'),
        (5, 'Istituzione dell\'Eucaristia', 'Lc 22,14-20', 'thursday'),
    ]
}

MYSTERY_TITLES = {
    'it': {
        'joyful': 'Misteri gaudiosi',
        'sorrowful': 'Misteri dolorosi',
        'glorious': 'Misteri gloriosi',
        'luminous': 'Misteri luminosi'
    },
    'en': {
        'joyful': 'Joyful Mysteries',
        'sorrowful': 'Sorrowful Mysteries',
        'glorious': 'Glorious Mysteries',
        'luminous': 'Luminous Mysteries'
    },
    'es': {
        'joyful': 'Misterios gozosos',
        'sorrowful': 'Misterios dolorosos',
        'glorious': 'Misterios gloriosos',
        'luminous': 'Misterios luminosos'
    },
    'pt': {
        'joyful': 'Mistérios gozosos',
        'sorrowful': 'Mistérios dolorosos',
        'glorious': 'Mistérios gloriosos',
        'luminous': 'Mistérios luminosos'
    }
}

if __name__ == '__main__':
    # 1. Assicura cartelle
    os.makedirs('data', exist_ok=True)

    # 2. Rimuove il DB se esistente
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 3. Legge schema.sql
    if not os.path.exists(SCHEMA_PATH):
        print(f"Errore: {SCHEMA_PATH} non trovato")
        sys.exit(1)

    with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
        schema_sql = f.read()

    cursor.executescript(schema_sql)

    # 4. Popola prayer
    prayer_rows = []
    for p in PRAYERS:
        for lang, text in p['text'].items():
            prayer_rows.append((p['key'], lang, p['category'], p['title'], text, None))

    cursor.executemany(
        'INSERT INTO prayer (key, lang, category, title, text, audio_tts_hint) VALUES (?, ?, ?, ?, ?, ?)',
        prayer_rows
    )

    # 5. Popola rosary_mystery
    mystery_rows = []
    for lang in MYSTERY_TITLES.keys():
        for mystery_type, tuples in MYSTERY_DEFS.items():
            for number, title_it, scripture_ref, days in tuples:
                if lang == 'it':
                    title = f'{MYSTERY_TITLES[lang][mystery_type]} - {title_it}'
                else:
                    title = f'{MYSTERY_TITLES[lang][mystery_type]} - {title_it}'
                description = f'{title} ({scripture_ref})'
                mystery_rows.append((mystery_type, number, lang, title, description, scripture_ref, days))

    cursor.executemany(
        'INSERT INTO rosary_mystery (type, number, lang, title, description, scripture_ref, recommended_days) VALUES (?, ?, ?, ?, ?, ?, ?)',
        mystery_rows
    )

    # 5b. Popola via_crucis
    from populate_via_crucis import get_via_crucis_rows
    cursor.executemany(
        'INSERT INTO via_crucis (station, lang, title, meditation, prayer, scripture_ref) VALUES (?, ?, ?, ?, ?, ?)',
        get_via_crucis_rows()
    )
    print(f"Via Crucis: {len(get_via_crucis_rows())} righe inserite")

    # 5c. Popola novena
    from populate_novene import get_novena_rows
    cursor.executemany(
        'INSERT INTO novena (novena_key, day, lang, title, intention, prayer, scripture_ref) VALUES (?, ?, ?, ?, ?, ?, ?)',
        get_novena_rows()
    )
    print(f"Novene: {len(get_novena_rows())} righe inserite")

    # 5d. Popola feast_calendar
    from populate_feast_calendar import get_feast_calendar_rows
    feast_rows = get_feast_calendar_rows()
    cursor.executemany(
        'INSERT INTO feast_calendar (month, day, saint_name, names_it, names_en, names_es, names_pt, feast_rank) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
        feast_rows
    )
    print(f"Feast calendar: {len(feast_rows)} righe inserite")

    # 5e. Popola saint_greeting
    from populate_saint_greeting import get_saint_greeting_rows
    greeting_rows = get_saint_greeting_rows()
    cursor.executemany(
        'INSERT INTO saint_greeting (saint_name, lang, greeting_short, greeting_long, fun_fact) VALUES (?, ?, ?, ?, ?)',
        greeting_rows
    )
    print(f"Saint greeting: {len(greeting_rows)} righe inserite")

    # 5f. Popola liturgical_day
    print("Fetching liturgical day data...")
    from fetch_liturgical_day import get_all_rows as get_liturgical_rows
    liturgical_rows = get_liturgical_rows()
    cursor.executemany(
        '''INSERT INTO liturgical_day
           (date, season, week_number, day_of_week, celebration_name,
            celebration_type, liturgical_color, is_sunday, is_holy_day)
           VALUES (:date, :season, :week_number, :day_of_week, :celebration_name,
                   :celebration_type, :liturgical_color, :is_sunday, :is_holy_day)''',
        liturgical_rows
    )
    print(f"Liturgical day: {len(liturgical_rows)} righe inserite")

    conn.commit()

    # 6. Fetch gospel and saints for entire year 2026
    print("\nFetching gospel readings for 2026...")
    from fetch_gospel import fetch_gospel_day
    from fetch_saints import fetch_saint_day
    from datetime import datetime, timedelta
    import json

    start_date = datetime.strptime('2026-01-01', '%Y-%m-%d')
    end_date = datetime.strptime('2026-12-31', '%Y-%m-%d')
    
    current_date = start_date
    fetched_gospels = 0
    fetched_saints = 0
    
    while current_date <= end_date:
        date_str = current_date.strftime('%Y-%m-%d')
        
        # Fetch gospel
        gospel_result = fetch_gospel_day(date_str)
        if gospel_result:
            fetched_gospels += 1
            if fetched_gospels % 50 == 0:
                print(f"  Fetched {fetched_gospels} gospels...")
        
        # Fetch saint
        saint_result = fetch_saint_day(date_str)
        if saint_result:
            fetched_saints += 1
            if fetched_saints % 50 == 0:
                print(f"  Fetched {fetched_saints} saints...")
        
        current_date += timedelta(days=1)
    
    print(f"Fetched {fetched_gospels} gospels and {fetched_saints} saints")
    
    # 7. Insert gospel and saint data from raw files
    print("\nInserting gospel data into database...")
    gospel_dir = 'data/raw/gospel'
    if os.path.exists(gospel_dir):
        gospel_files = sorted([f for f in os.listdir(gospel_dir) if f.endswith('.json')])
        gospel_rows = []
        for filename in gospel_files:
            filepath = os.path.join(gospel_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            date_str = data.get('date')
            reference = data.get('gospel_ref', '')
            reading_1_ref = data.get('reading_1_ref', '')
            source = data.get('season', '')
            for lang in ['it', 'en', 'es', 'pt']:
                gospel_text = data.get(f'gospel_text_{lang}', '')
                reading_1_text = data.get(f'reading_1_text_{lang}', '')
                gospel_rows.append((date_str, lang, reference, gospel_text, reading_1_ref, reading_1_text, source))

        cursor.executemany(
            'INSERT INTO gospel (date, lang, reference, text, reading_1_ref, reading_1_text, source) VALUES (?, ?, ?, ?, ?, ?, ?)',
            gospel_rows
        )
    
    print("Inserting saint data into database...")
    saint_dir = 'data/raw/saints'
    if os.path.exists(saint_dir):
        saint_files = sorted([f for f in os.listdir(saint_dir) if f.endswith('.json')])
        saint_rows = []
        for filename in saint_files:
            filepath = os.path.join(saint_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            date_str = data.get('date')
            for lang in ['it', 'en', 'es', 'pt']:
                name = data.get(f'name_{lang}', '')
                bio = data.get(f'bio_{lang}', '')
                feast_type = data.get(f'feast_type_{lang}', '')
                wikipedia_url = data.get(f'wikipedia_url_{lang}', '')

                saint_rows.append((date_str, lang, name, feast_type, bio, wikipedia_url))

        cursor.executemany(
            'INSERT INTO saint (date, lang, name, feast_type, short_bio, wikipedia_url) VALUES (?, ?, ?, ?, ?, ?)',
            saint_rows
        )
    
    conn.commit()

    # 8. Final summary
    counts = {}
    for table in ('prayer', 'rosary_mystery', 'gospel', 'saint', 'via_crucis', 'novena',
                  'liturgical_day', 'feast_calendar', 'saint_greeting'):
        cursor.execute(f'SELECT COUNT(*) FROM {table}')
        counts[table] = cursor.fetchone()[0]

    expected = {
        'prayer': 68,
        'rosary_mystery': 80,
        'gospel': 1460,
        'saint': 1460,
        'via_crucis': 56,
        'novena': 180,
        'liturgical_day': 365,
        'feast_calendar': 140,
        'saint_greeting': 400,
    }

    print('\n=== Database Summary ===')
    print(f'DB creato in {DB_PATH}')
    print(f'{"Tabella":<20} {"Righe":>8} {"Attese":>8} {"Stato":>6}')
    print('-' * 46)
    for table, count in counts.items():
        exp = expected.get(table, '?')
        ok = 'OK' if count >= exp else 'KO'
        print(f'{table:<20} {count:>8} {exp:>8} {ok:>6}')
    print('======================')

    conn.close()
