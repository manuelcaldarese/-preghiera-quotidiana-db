#!/usr/bin/env python3
"""
Populates prayer table with standard liturgical prayers in 4 languages
"""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data" / "prayers.db"

PRAYERS = {
    'daily': {
        'lords_prayer': {
            'title': {'it': 'Padre Nostro', 'en': 'Our Father', 'es': 'Padre Nuestro', 'pt': 'Pai Nosso'},
            'text': {
                'it': 'Padre nostro, che sei nei cieli,\nsia santificato il tuo nome,\nvenga il tuo regno,\nsia fatta la tua volontà,\ncome in cielo così in terra.\nDacci oggi il nostro pane quotidiano,\ne rimetti a noi i nostri debiti\ncome noi li rimettiamo ai nostri debitori.\nE non ci indurre in tentazione,\nma liberaci dal male.\nAmen.',
                'en': 'Our Father, who art in heaven,\nhallowed be thy name;\nthy kingdom come;\nthy will be done on earth as it is in heaven.\nGive us this day our daily bread;\nand forgive us our trespasses\nas we forgive those who trespass against us;\nand lead us not into temptation,\nbut deliver us from evil.\nAmen.',
                'es': 'Padre nuestro, que estás en el cielo,\nsantificado sea tu nombre,\nvenga a nosotros tu reino,\nhágase tu voluntad\nen la tierra como en el cielo.\nDanos hoy nuestro pan de cada día,\nperdona nuestras ofensas,\ncomo también nosotros perdonamos\na los que nos ofenden.\nNo nos dejes caer en tentación\ny líbranos del mal.\nAmén.',
                'pt': 'Pai nosso, que estais no céu,\nsantificado seja o vosso nome,\nvenha a nós o vosso reino,\nfaça-se a vossa vontade,\nna terra como no céu.\nO pão nosso de cada dia nos daí hoje,\nperdoai-nos as nossas dívidas,\nassi como nós perdoamos aos nossos devedores,\ne não nos deixeis cair em tentação,\nmas livrai-nos do mal.\nAmém.'
            }
        },
        'hail_mary': {
            'title': {'it': 'Ave Maria', 'en': 'Hail Mary', 'es': 'Avemaría', 'pt': 'Ave Maria'},
            'text': {
                'it': 'Ave, o Maria, piena di grazia,\nil Signore è con te;\ntu sei benedetta fra le donne,\ne benedetto è il frutto del tuo seno, Gesù.\nSanta Maria, Madre di Dio,\nprega per noi peccatori,\nadesso e nell\'ora della nostra morte.\nAmen.',
                'en': 'Hail Mary, full of grace,\nthe Lord is with thee;\nblessed art thou amongst women,\nand blessed is the fruit of thy womb, Jesus.\nHoly Mary, Mother of God,\npray for us sinners,\nnow and at the hour of our death.\nAmen.',
                'es': 'Dios te salve, María, llena eres de gracia,\nEl Señor es contigo;\nBendita tú eres entre todas las mujeres,\ny bendito es el fruto de tu vientre, Jesús.\nSanta María, Madre de Dios,\nruega por nosotros los pecadores,\nahora y en la hora de nuestra muerte.\nAmén.',
                'pt': 'Ave Maria, cheia de graças,\no Senhor é convosco,\nbenção sois vós entre as mulheres,\ne benção é o fruto do vosso ventre, Jesus.\nSanta Maria, Mãe de Deus,\nrogar por nós pecadores,\nagora e na hora da nossa morte.\nAmém.'
            }
        },
        'glory_be': {
            'title': {'it': 'Gloria al Padre', 'en': 'Glory Be', 'es': 'Gloria al Padre', 'pt': 'Glória ao Pai'},
            'text': {
                'it': 'Gloria al Padre,\ne al Figlio,\ne allo Spirito Santo.\nCom\'era nel principio,\ne ora, e sempre,\nei secoli dei secoli.\nAmen.',
                'en': 'Glory be to the Father,\nand to the Son,\nand to the Holy Spirit.\nAs it was in the beginning,\nis now, and ever shall be,\nworld without end.\nAmen.',
                'es': 'Gloria al Padre,\ny al Hijo,\ny al Espíritu Santo.\nComo era en el principio,\nahora y siempre,\ny por los siglos de los siglos.\nAmén.',
                'pt': 'Glória ao Pai,\ne ao Filho,\ne ao Espírito Santo.\nComo era no princípio,\nagora e sempre,\ne pelos séculos dos séculos.\nAmém.'
            }
        },
        'apostles_creed': {
            'title': {'it': 'Credo degli Apostoli', 'en': 'Apostles\' Creed', 'es': 'Credo de los Apóstoles', 'pt': 'Creio dos Apóstolos'},
            'text': {
                'it': 'Credo in Dio, Padre onnipotente, creatore del cielo e della terra.\nCredo in Gesù Cristo, suo unico Figlio, nostro Signore,\nil quale fu concepito di Spirito Santo, nacque da Maria Vergine,\npatì sotto Ponzio Pilato, fu crocifisso, morì e fu sepolto;\ndiscese agli inferi; il terzo giorno risuscitò da morte.\nSalì al cielo, siede alla destra di Dio Padre onnipotente.\nDi là verrà a giudicare i vivi e i morti.\nCredo nello Spirito Santo,\nla santa Chiesa cattolica, la comunione dei santi,\nla remissione dei peccati,\nla risurrezione della carne,\nla vita eterna.\nAmen.',
                'en': 'I believe in God, the Father almighty, creator of heaven and earth.\nI believe in Jesus Christ, his only Son, our Lord,\nwho was conceived by the Holy Spirit, born of the Virgin Mary,\nsuffered under Pontius Pilate, was crucified, died, and was buried;\nhe descended to the dead. On the third day he rose again;\nhe ascended into heaven, he is seated at the right hand of the Father,\nand he will come to judge the living and the dead.\nI believe in the Holy Spirit,\nthe holy catholic Church, the communion of saints,\nthe forgiveness of sins, the resurrection of the body,\nand the life everlasting.\nAmen.',
                'es': 'Creo en Dios, Padre todopoderoso, Creador del cielo y de la tierra.\nCreo en Jesucristo, su único Hijo, nuestro Señor,\nque fue concebido por obra y gracia del Espíritu Santo,\nnacido de Santa María Virgen,\nque padeció bajo el poder de Poncio Pilato,\nfue crucificado, muerto y sepultado,\ndescendió a los infiernos, y al tercer día resucitó;\nsubió a los cielos y está sentado a la diestra de Dios Padre todopoderoso,\ny desde allí ha de venir a juzgar a los vivos y a los muertos.\nCreo en el Espíritu Santo,\nla santa Iglesia católica, la comunión de los santos,\nla remisión de los pecados,\nla resurrección de la carne\ny la vida eterna.\nAmén.',
                'pt': 'Creio em Deus Pai todo-poderoso, criador do céu e da terra.\nCreio em Jesus Cristo, seu único Filho, nosso Senhor,\nque foi concebido pelo Espírito Santo e nasceu da Virgem Maria,\npadeceu sob Pôncio Pilatos, foi crucificado, morto e sepultado,\ndesceu à mansão dos mortos; ressuscitou ao terceiro dia,\nsubiu aos céus, está sentado à direita de Deus Pai todo-poderoso,\nde onde há de vir a julgar os vivos e os mortos.\nCreio no Espírito Santo,\nna santa Igreja Católica, na comunhão dos santos,\nna remissão dos pecados, na ressurreição da carne,\nna vida eterna.\nAmém.'
            }
        },
        'act_of_contrition': {
            'title': {'it': 'Atto di Dolore', 'en': 'Act of Contrition', 'es': 'Acto de Contrición', 'pt': 'Ato de Contrição'},
            'text': {
                'it': 'O mio Dio, mi pento sinceramente di averti offeso\ne detesto tutti i miei peccati,\nperché temendo il tuo castigo\nma soprattutto perché ti amo\ne voglio amarti per sempre.\nCon tutto il cuore mi propongo,\naiutato dalla tua grazia,\ndi non offenderti mai più\ne di evitare le occasioni di peccato.\nAmen.',
                'en': 'O my God, I am heartily sorry for having offended you,\nand I detest all my sins,\nbecause I dread the loss of heaven\nand the pains of hell;\nbut most of all because I have offended you, my God,\nwho are all good and deserving of all my love.\nI firmly resolve, with the help of your grace,\nto confess my sins, to do penance,\nand to amend my life.\nAmen.',
                'es': 'Dios mío, me arrepiento sinceramente de haber te ofendido\ny detesto todos mis pecados,\nno solo porque merezcan tu castigo,\nsino principalmente porque te he ofendido a ti,\nque eres infinitamente bueno\ny digno de ser amado sobre todas las cosas.\nPropongo firmemente, con la ayuda de tu gracia,\nno volver a pecar\ny evitar las ocasiones de pecado.\nAmén.',
                'pt': 'Meu Deus, arrependo-me sinceramente de vos ter ofendido\ne detesto todos os meus pecados,\nnão só porque merecem o vosso castigo,\nmas principalmente porque vos ofendi,\na vós que sois infinitamente bom\ne digno de ser amado acima de todas as coisas.\nProponho firmemente, com o auxílio da vossa graça,\nnão mais vos ofender\ne evitar as ocasiões de pecado.\nAmém.'
            }
        },
    },
    'marian': {
        'angelus': {
            'title': {'it': 'Angelus', 'en': 'Angelus', 'es': 'Angelus', 'pt': 'Angélus'},
            'text': {
                'it': 'L\'Angelo del Signore annunziò a Maria.\nE concepì di Spirito Santo.\nAve Maria, piena di grazia...\n\nEcco l\'ancella del Signore.\nAvvenga di me secondo la tua parola.\nAve Maria, piena di grazia...\n\nE il Verbo si fece carne.\nE abitò tra noi.\nAve Maria, piena di grazia...\n\nPrega per noi, santa Madre di Dio.\nAffinché siamo resi degni delle promesse di Cristo.\n\nSiamo in preghiera:\nO Signore, che per l\'Incarnazione del tuo Figlio\nha voluto salvare l\'umanità,\naccordi ai tuoi servi di professare la vera fede\ne di lodarti con opere di carità.\nPer lo stesso Cristo nostro Signore.\nAmen.',
                'en': 'The Angel of the Lord announced to Mary.\nAnd she conceived of the Holy Spirit.\nHail Mary, full of grace...\n\nBehold the handmaid of the Lord.\nBe it done unto me according to thy word.\nHail Mary, full of grace...\n\nAnd the Word was made flesh.\nAnd dwelt among us.\nHail Mary, full of grace...\n\nPray for us, O Holy Mother of God.\nThat we may be made worthy of the promises of Christ.\n\nLet us pray:\nPour forth, we beseech thee, O Lord,\nthy grace into our hearts,\nthat we to whom the Incarnation of Christ thy Son\nwas made known by the message of an Angel,\nmay by his Passion and Cross\nbe brought to the glory of His Resurrection.\nThrough the same Christ our Lord.\nAmen.',
                'es': 'El ángel del Señor anunció a María.\nY concibió por obra del Espíritu Santo.\nDios te salve, María, llena eres de gracia...\n\nHe aquí la esclava del Señor.\nHágase en mí según tu palabra.\nDios te salve, María, llena eres de gracia...\n\nY el Verbo se hizo carne.\nY habitó entre nosotros.\nDios te salve, María, llena eres de gracia...\n\nRuega por nosotros, Santa Madre de Dios.\nPara que seamos dignos de alcanzar las promesas de Jesucristo.\n\nOremus:\nDerrama, Señor, tu gracia en nuestras almas\npara que, conociendo el misterio de la Encarnación de tu Hijo\npor el anuncio del ángel,\nllegemos por su Pasión y su Cruz\na la gloria de la Resurrección.\nPor Jesucristo nuestro Señor.\nAmén.',
                'pt': 'O Anjo do Senhor anunciou a Maria.\nE ela concebeu do Espírito Santo.\nAve Maria, cheia de graças...\n\nEis aqui a escrava do Senhor.\nFaça-se em mim segundo a vossa palavra.\nAve Maria, cheia de graças...\n\nE o Verbo se fez carne.\nE habitou entre nós.\nAve Maria, cheia de graças...\n\nRogai por nós, Santa Mãe de Deus.\nPara que seamos dignos das promessas de Cristo.\n\nOremus:\nDerramae, Senhor, vossa graça nas nossas almas,\npara que, conhecendo o mistério da Encarnação de vosso Filho\npelo anúncio do Anjo,\ncheguemos pela sua Paixão e pela sua Cruz\nà glória da Ressurreição.\nPelo mesmo Cristo nosso Senhor.\nAmém.'
            }
        },
        'regina_coeli': {
            'title': {'it': 'Regina Coeli', 'en': 'Regina Coeli', 'es': 'Regina Coeli', 'pt': 'Rainha do Céu'},
            'text': {
                'it': 'Regina del cielo, rallegrati, alleluia.\nPerché colui che meritasti di portare, alleluia,\nè risorto come disse, alleluia.\nPrega per noi Dio, alleluia.\n\nGoditi, o Vergine Maria, alleluia.\nPerché il Signore è veramente risorto, alleluia.\n\nGloriam, Signore, che sei risorto dai morti,\nch\'hai liberato il genere umano.\nOra concedi la pace al mondo intero\ne permettici di giungere alla gloria eterna.\nAmen.',
                'en': 'Queen of Heaven, rejoice, alleluia.\nFor He whom thou wast meet to bear, alleluia,\nHath risen as He said, alleluia.\nPray for us to God, alleluia.\n\nRejoice and be glad, O Virgin Mary, alleluia.\nBecause the Lord is truly risen, alleluia.\n\nGlory be to the Lord, who has risen from the dead,\nwho has liberated mankind.\nNow grant peace throughout the world\nand allow us to reach eternal glory.\nAmen.',
                'es': 'Reina del cielo, alégrate, aleluya.\nPorque el que mereciste llevar, aleluya,\nha resucitado como dijo, aleluya.\nRuega por nosotros a Dios, aleluya.\n\nGoza y alégrate, Virgen María, aleluya.\nPorque el Señor ha resucitado verdaderamente, aleluya.\n\nGloria sea al Señor que ha resucitado,\nque ha liberado al género humano.\nOtorga paz a todo el mundo\ny permítenos llegar a la gloria eterna.\nAmén.',
                'pt': 'Rainha do Céu, alegrai-vos, aleluia.\nPorque aquele que merecestes levar, aleluia,\nresuscitou como prometeu, aleluia.\nRogai por nós ao Senhor, aleluia.\n\nRegozijai-vos e alegrai-vos, Virgem Maria, aleluia.\nPorque o Senhor verdadeiramente ressuscitou, aleluia.\n\nGlória seja ao Senhor que ressuscitou,\nque libertou o gênero humano.\nConcedei paz a todo o mundo\ne permitidos que cheguemos à glória eterna.\nAmém.'
            }
        },
        'memorare': {
            'title': {'it': 'Memorare', 'en': 'Memorare', 'es': 'Memorare', 'pt': 'Memorare'},
            'text': {
                'it': 'Ricordati, o clementissima Vergine Maria,\nche non si è mai sentito dire che nessuno,\nche sia ricorso alla tua protezione,\nimplorato il tuo aiuto,\nchiesto la tua intercessione,\nsia stato abbandonato da te.\nIncoraggiato da questa fiducia io ricorro a te,\nVergine fra tutte le vergini madre mia,\ne vengo innanzi a te penitente e pieno di peccati.\nNon disprezzare le mie suppliche,\nVergine madre misericordiosa,\nma ascoltami benignamente.\nAmen.',
                'en': 'Remember, O most gracious Virgin Mary,\nthat never was it known\nthat anyone who fled to thy protection,\nimplored thy help, or sought thine intercession,\nwas left unaided.\nInspired by this confidence,\nI fly unto thee, O Virgin of virgins, my Mother.\nTo thee I come, before thee I stand,\nsinful and sorrowful.\nO Mother of the Word Incarnate,\ndespise not my petitions,\nbut in thy mercy hear and answer me.\nAmen.',
                'es': 'Acuérdate, oh Madre de Dios clementísima,\nque jamas se ha oído decir\nque nadie haya acudido bajo tu protección,\nimplorado tu auxilio,\nreclamado tu intercesión,\ny haya sido desamparado.\nAlentado pues de esta confianza,\na ti recurro, Virgen entre todas las Vírgenes, Madre mía,\ny a ti dirijo mi oración,\narrodillado, arrepentido y lleno de pecados.\nNo desdeñes mis súplicas,\noh Madre de Dios,\nantes bien escúchalas benignamente.\nAmén.',
                'pt': 'Lembremos, ó clementíssima Virgem Maria,\nque nunca se ouviu dizer\nque alguém tivesse recorrido a vossa proteção,\nimplorado vosso auxílio,\nsupplicado vossa intercessão,\ne tivesse sido desamparado.\nAnimado por esta confiança,\na vós recorro, Virgem entre todas as Virgens, Mãe minha,\ne a vós dirijo minha oração,\najoelhado, arrependido e cheio de pecados.\nNão desprezeis meus rogos,\nó Mãe de Deus,\nantes pelo contrário ouvi-me benignamente.\nAmém.'
            }
        },
        'salve_regina': {
            'title': {'it': 'Salve Regina', 'en': 'Salve Regina', 'es': 'Salve Regina', 'pt': 'Salve Rainha'},
            'text': {
                'it': 'Salve, Regina, madre di misericordia,\nvita, dolcezza e speranza nostra, salve.\nA te ricorriamo, esuli figli di Eva;\na te sospiriamo, gementi e piangenti in questa valle di lacrime.\nAva, dunque, avvocata nostra;\nvolgi a noi quegli occhi misericordiosi;\ne mostraci, dopo questo esilio, Gesù,\nfrutto benedetto del tuo seno.\nODolce, o pia, o dolce Vergine Maria.\nAmen.',
                'en': 'Hail, holy Queen, Mother of mercy,\nhail, our life, our sweetness, and our hope.\nTo thee do we cry, poor banished children of Eve;\nto thee do we send up our sighs,\nourning and weeping in this vale of tears.\nTurn, then, most gracious advocate,\nthine eyes of mercy toward us;\nand after this our exile,\nshow unto us the blessed fruit of thy womb, Jesus.\nO clement, O loving, O sweet Virgin Mary.\nPray for us, O holy Mother of God,\nthat we may be made worthy of the promises of Christ.\nAmen.',
                'es': 'Dios te salve Reina y Madre de misericordia,\nvida, dulzura y esperanza nuestra; Dios te salve.\nA ti clamamos los desterrados hijos de Eva;\na ti suspiramos, gimiendo y llorando en este valle de lágrimas.\nEa, pues, Señora, abogada nuestra,\nvuelve a nosotros esos tus ojos misericordiosos,\ny después de este destierro muéstranos a Jesús,\nfruto bendito de tu vientre.\n¡Oh clementísima! ¡Oh piadosa! ¡Oh dulce Virgen María!\nAmén.',
                'pt': 'Salve Rainha, Mãe de misericórdia,\nvida, doçura e esperança nossa, salve!\nA vós clamamos os filhos de Eva, como desterrados;\na vós suspiramos, gemendo e chorando neste vale de lágrimas.\nPortanto, ó nossa Salvadora, volvei para nós\nvossos olhos misericordiosos;\ne depois deste desterro, mostrai-nos Jesus,\nfruto bendito de vosso ventre.\n¡Ó clemente! ¡Ó piedosa! ¡Ó doce Virgem Maria!\nAmen.'
            }
        },
    },
    'meal': {
        'grace_before_meals': {
            'title': {'it': 'Preghiera prima dei pasti', 'en': 'Grace Before Meals', 'es': 'Gracia antes de la Comida', 'pt': 'Ação de graças antes das refeições'},
            'text': {
                'it': 'Benedetto sei tu, Signore, nostro Dio,\nche nutri i poveri e i ricchi.\nCome hai nutrito il popolo nel deserto\nviene ancora nutrita tutta la creazione dalla tua generosità.\nBenedetto sei tu, Signore,\nte la tua bontà e clemenza siano un beneficio per tutti gli uomini.\nAmen.',
                'en': 'Blessed are You, O Lord our God,\nking of the universe, who brings forth bread from the earth.\nBless this food and those who share it.\nGive us grateful hearts and help us to share our blessings with others.\nAmen.',
                'es': 'Bendito seáis, Señor, Dios nuestro,\nsoberano del universo, que produces el pan de la tierra.\nBendice este alimento y a los que lo compartimos.\nDanos corazones agradecidos\ny ayúdanos a compartir nuestras bendiciones con otros.\nAmén.',
                'pt': 'Bendito sois, Senhor, Deus nosso,\nsoberano do universo,\nque fazeis brotar o pão da terra.\nAbençoai este alimento e aos que o partilhamos.\nDai-nos corações gratos\ne ajudai-nos a partilhar nossas bênçãos com outros.\nAmém.'
            }
        },
        'grace_after_meals': {
            'title': {'it': 'Preghiera dopo i pasti', 'en': 'Grace After Meals', 'es': 'Gracia después de la Comida', 'pt': 'Ação de graças após as refeições'},
            'text': {
                'it': 'Ti ringraziamo, sempre e dovunque, Signore nostro,\nDio del cielo e della terra.\nNoi ti ringraziamo per questa mensa\ne per tutti i benefici che ci hai dato.\nSempre ti sia gloria con il Padre e lo Spirito Santo,\nora e sempre, nei secoli dei secoli.\nAmen.',
                'en': 'We give Thee thanks,\nAlmighty God,\nfor these and all Thy benefits,\nwhich we have received from Thy boundless generosity.\nThrough Christ our Lord.\nAmen.',
                'es': 'Os damos gracias, Señor,\npor estos alimentos y todos los beneficios\nque hemos recibido de vuestra infinita generosidad.\nA través de Cristo nuestro Señor.\nAmén.',
                'pt': 'Vos damos graças, Senhor,\npor este alimento e por todos os benefícios\nque recebemos da vossa infinita generosidade.\nPor Cristo nosso Senhor.\nAmém.'
            }
        },
    },
    'rosary': {
        'fatima_prayer': {
            'title': {'it': 'Preghiera di Fatima', 'en': 'Fatima Prayer', 'es': 'Oración de Fátima', 'pt': 'Oração de Fátima'},
            'text': {
                'it': 'O mio Gesù, perdona i nostri peccati,\npreservaci dal fuoco dell\'inferno;\nconduci in cielo tutte le anime,\nspecialmente le più bisognose della tua misericordia.\nAmen.',
                'en': 'O Jesus, forgive us our sins,\nsave us from the fires of Hell,\nlead all souls to Heaven,\nespecially those in greatest need of Thy mercy.\nAmen.',
                'es': 'Oh Jesús mío, perdona nuestros pecados,\nlíbranos del fuego del infierno,\nleva al cielo a todas las almas,\nespecialmente aquellas que más necesitan de tu misericordia.\nAmén.',
                'pt': 'Ó Jesus meu, perdoai os nossos pecados,\nlivrai-nos do fogo do inferno,\nlevai ao céu todas as almas,\nespecialmente as que mais precisam da vossa misericórdia.\nAmém.'
            }
        },
        'hail_holy_queen': {
            'title': {'it': 'Salve Regina del Rosario', 'en': 'Hail Holy Queen', 'es': 'Dios te Salve Reina', 'pt': 'Salve Rainha'},
            'text': {
                'it': 'Salve, Regina, madre di misericordia,\nvita, dolcezza e speranza nostra.\nA te ricorriamo, esuli figli di Eva,\na te sospiriamo, gementi e piangenti\nin questa valle di lacrime.\nAva, dunque, avvocata nostra,\nvolgi a noi quegli occhi misericordiosi,\ne mostraci Gesù, frutto benedetto\ndel tuo seno, dopo questo esilio.\nO clemente, o pia.\nAmen.',
                'en': 'Hail, holy Queen, Mother of mercy,\nour life, our sweetness, and our hope.\nTo thee do we cry, poor banished children of Eve;\nto thee do we send up our sighs,\nmourning and weeping in this vale of tears.\nTurn, then, O most gracious advocate,\nthine eyes of mercy toward us,\nand after this our exile,\nshow unto us the blessed fruit of thy womb, Jesus.\nO clement, O loving, O sweet Virgin Mary.\nAmen.',
                'es': 'Salve, Reina, Madre de misericordia,\nlife, la dulzura y la esperanza nuestra.\nA ti clamamos los desterrados hijos de Eva;\na ti suspiramos, gimiendo\ny llorando, en este valle de lágrimas.\nAvogada nuestra, vuelve a nosotros\nesos ojos misericordiosos,\ny después de este destierro,\nmuéstranos a Jesús,\nfruto bendito de tu vientre.\nOh clemente, oh piadosa.\nAmén.',
                'pt': 'Salve, Rainha, Mãe de misericórdia,\nvida, doçura e esperança nossa,\nsalve!\nA vós clamamos os filhos de Eva,\ncomo desterrados;\na vós suspiramos, gemendo\ne chorando neste vale de lágrimas.\nPorque, ó Salvadora nossa,\nvolvei para nós\nvossos olhos misericordiosos;\ne depois deste desterro,\nmostrai-nos Jesus,\nfruto bendito de vosso ventre.\nÓ clemente, ó piedosa.\nAmém.'
            }
        },
    }
}

def populate_prayers(db_path):
    """Insert all prayers into the prayer table"""
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    inserted = 0
    for category, prayers in PRAYERS.items():
        for prayer_key, prayer_data in prayers.items():
            for lang in ['it', 'en', 'es', 'pt']:
                title = prayer_data['title'].get(lang, '')
                text = prayer_data['text'].get(lang, '')
                
                if title and text:
                    cur.execute("""
                        INSERT INTO prayer (key, lang, category, title, text)
                        VALUES (?, ?, ?, ?, ?)
                    """, (prayer_key, lang, category, title, text))
                    inserted += 1
    
    conn.commit()
    conn.close()
    print(f"Populated {inserted} prayers")

if __name__ == '__main__':
    populate_prayers(DB_PATH)
