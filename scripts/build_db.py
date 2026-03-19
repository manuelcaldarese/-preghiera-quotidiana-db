#!/usr/bin/env python3
import os
import sqlite3
import sys

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
    }
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

    conn.commit()

    # 6. Riepilogo
    cursor.execute('SELECT COUNT(*) FROM prayer')
    prayer_count = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM rosary_mystery')
    mystery_count = cursor.fetchone()[0]

    print('DB creato in', DB_PATH)
    print('Rig...')
    print(f' - prayer: {prayer_count} righe')
    print(f' - rosary_mystery: {mystery_count} righe')

    conn.close()
