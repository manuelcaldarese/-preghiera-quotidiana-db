#!/usr/bin/env python3
"""
Populates rosary_mystery table with all rosary mysteries in 4 languages
"""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data" / "prayers.db"

MYSTERIES = {
    'joyful': [
        {
            'number': 1,
            'title': {'it': 'L\'Annunciazione', 'en': 'The Annunciation', 'es': 'La Anunciación', 'pt': 'A Anunciação'},
            'description': {
                'it': 'L\'arcangelo Gabriele annuncia a Maria che sarà madre del Figlio di Dio.',
                'en': 'The Angel Gabriel announces to Mary that she will be the mother of the Son of God.',
                'es': 'El arcángel Gabriel anuncia a María que será la madre del Hijo de Dios.',
                'pt': 'O arcanjo Gabriel anuncia a Maria que ela será a mãe do Filho de Deus.'
            },
            'scripture_ref': 'Luke 1:26-38',
            'recommended_days': 'Monday, Saturday'
        },
        {
            'number': 2,
            'title': {'it': 'La Visitazione', 'en': 'The Visitation', 'es': 'La Visitación', 'pt': 'A Visitação'},
            'description': {
                'it': 'Maria visita la cugina Elisabetta e cantano insieme le lodi di Dio.',
                'en': 'Mary visits her cousin Elizabeth and they sing together the praises of God.',
                'es': 'María visita a su prima Isabel y juntas cantan las alabanzas de Dios.',
                'pt': 'Maria visita sua prima Isabel e juntas cantam os louvores de Deus.'
            },
            'scripture_ref': 'Luke 1:39-56',
            'recommended_days': 'Monday, Saturday'
        },
        {
            'number': 3,
            'title': {'it': 'La Nascita di Gesù', 'en': 'The Nativity of Jesus', 'es': 'El Nacimiento de Jesús', 'pt': 'O Nascimento de Jesus'},
            'description': {
                'it': 'Gesù nasce a Betlemme e Maria lo adagia nella mangiatoia.',
                'en': 'Jesus is born in Bethlehem and Mary lays him in the manger.',
                'es': 'Jesús nace en Belén y María lo coloca en el pesebre.',
                'pt': 'Jesus nasce em Belém e Maria o coloca no presépio.'
            },
            'scripture_ref': 'Luke 2:1-20',
            'recommended_days': 'Monday, Saturday'
        },
        {
            'number': 4,
            'title': {'it': 'La Presentazione al Tempio', 'en': 'The Presentation of Jesus at the Temple', 'es': 'La Presentación de Jesús en el Templo', 'pt': 'A Apresentação de Jesus no Templo'},
            'description': {
                'it': 'Maria e Giuseppe presentano Gesù al tempio secondo la legge giudaica.',
                'en': 'Mary and Joseph present Jesus at the temple according to Jewish law.',
                'es': 'María y José presentan a Jesús en el templo según la ley judía.',
                'pt': 'Maria e José apresentam Jesus no templo segundo a lei judaica.'
            },
            'scripture_ref': 'Luke 2:22-40',
            'recommended_days': 'Monday, Saturday'
        },
        {
            'number': 5,
            'title': {'it': 'Il ritrovamento di Gesù al Tempio', 'en': 'The Finding of Jesus at the Temple', 'es': 'El Hallazgo de Jesús en el Templo', 'pt': 'O Encontro de Jesus no Templo'},
            'description': {
                'it': 'Maria e Giuseppe trovano Gesù che insegna nel tempio dopo tre giorni di ricerche.',
                'en': 'Mary and Joseph find Jesus teaching in the temple after three days of searching.',
                'es': 'María y José encuentran a Jesús enseñando en el templo después de tres días de búsqueda.',
                'pt': 'Maria e José encontram Jesus ensinando no templo após três dias de busca.'
            },
            'scripture_ref': 'Luke 2:41-52',
            'recommended_days': 'Monday, Saturday'
        },
    ],
    'sorrowful': [
        {
            'number': 1,
            'title': {'it': 'L\'Agonia nell\'orto', 'en': 'The Agony in the Garden', 'es': 'La Agonía en el Huerto', 'pt': 'A Agonia no Jardim'},
            'description': {
                'it': 'Gesù prega nell\'orto del Getsemani, afflitto dall\'imminente sofferenza.',
                'en': 'Jesus prays in the Garden of Gethsemane, afflicted by his impending suffering.',
                'es': 'Jesús ora en el Huerto de Getsemaní, afligido por su sufrimiento inminente.',
                'pt': 'Jesus ora no Jardim do Getsêmani, aflito por seu sofrimento iminente.'
            },
            'scripture_ref': 'Matthew 26:36-56',
            'recommended_days': 'Tuesday, Friday'
        },
        {
            'number': 2,
            'title': {'it': 'La Flagellazione', 'en': 'The Scourging at the Pillar', 'es': 'La Flagelación', 'pt': 'A Flagelação'},
            'description': {
                'it': 'Gesù è fustigato dai soldati romani al comando di Pilato.',
                'en': 'Jesus is scourged by Roman soldiers at Pilate\'s command.',
                'es': 'Jesús es azotado por los soldados romanos por orden de Pilato.',
                'pt': 'Jesus é flagelado pelos soldados romanos por ordem de Pilato.'
            },
            'scripture_ref': 'Matthew 27:26',
            'recommended_days': 'Tuesday, Friday'
        },
        {
            'number': 3,
            'title': {'it': 'La Coronazione di spine', 'en': 'The Crowning with Thorns', 'es': 'La Coronación de espinas', 'pt': 'A Coroação de espinhos'},
            'description': {
                'it': 'I soldati coroano Gesù con spine a scherno della sua regalità.',
                'en': 'The soldiers crown Jesus with thorns in mockery of his kingship.',
                'es': 'Los soldados coronan a Jesús con espinas en burla de su realeza.',
                'pt': 'Os soldados coroam Jesus com espinhos em escárnio de sua realeza.'
            },
            'scripture_ref': 'Matthew 27:27-31',
            'recommended_days': 'Tuesday, Friday'
        },
        {
            'number': 4,
            'title': {'it': 'La Via Crucis', 'en': 'The Carrying of the Cross', 'es': 'La Carga de la Cruz', 'pt': 'O Caminho da Cruz'},
            'description': {
                'it': 'Gesù porta la croce al Calvario, incontrandosi con Maria e altre donne.',
                'en': 'Jesus carries his cross to Calvary, meeting Mary and other women on the way.',
                'es': 'Jesús carga con su cruz hacia el Calvario, encontrándose con María y otras mujeres.',
                'pt': 'Jesus carrega sua cruz para o Calvário, encontrando-se com Maria e outras mulheres.'
            },
            'scripture_ref': 'Luke 23:26-32',
            'recommended_days': 'Tuesday, Friday'
        },
        {
            'number': 5,
            'title': {'it': 'La Crocifissione', 'en': 'The Crucifixion', 'es': 'La Crucifixión', 'pt': 'A Crucificação'},
            'description': {
                'it': 'Gesù è crocifisso al Calvario e muore per la salvezza del mondo.',
                'en': 'Jesus is crucified at Calvary and dies for the salvation of the world.',
                'es': 'Jesús es crucificado en el Calvario y muere por la salvación del mundo.',
                'pt': 'Jesus é crucificado no calvário e morre pela salvação do mundo.'
            },
            'scripture_ref': 'Luke 23:33-46',
            'recommended_days': 'Tuesday, Friday'
        },
    ],
    'glorious': [
        {
            'number': 1,
            'title': {'it': 'La Risurrezione', 'en': 'The Resurrection', 'es': 'La Resurrección', 'pt': 'A Ressurreição'},
            'description': {
                'it': 'Gesù risorge dai morti il terzo giorno, vincendo il peccato e la morte.',
                'en': 'Jesus rises from the dead on the third day, conquering sin and death.',
                'es': 'Jesús resucita de los muertos al tercer día, venciendo el pecado y la muerte.',
                'pt': 'Jesus ressuscita da morte no terceiro dia, vencendo o pecado e a morte.'
            },
            'scripture_ref': 'Luke 24:1-12',
            'recommended_days': 'Wednesday, Sunday'
        },
        {
            'number': 2,
            'title': {'it': 'L\'Ascensione', 'en': 'The Ascension', 'es': 'La Ascensión', 'pt': 'A Ascensão'},
            'description': {
                'it': 'Gesù ascende al cielo quaranta giorni dopo la sua risurrezione.',
                'en': 'Jesus ascends to heaven forty days after his resurrection.',
                'es': 'Jesús asciende al cielo cuarenta días después de su resurrección.',
                'pt': 'Jesus ascende ao céu quarenta dias após sua ressurreição.'
            },
            'scripture_ref': 'Acts 1:6-11',
            'recommended_days': 'Wednesday, Sunday'
        },
        {
            'number': 3,
            'title': {'it': 'La Pentecoste', 'en': 'The Descent of the Holy Spirit', 'es': 'La Venida del Espíritu Santo', 'pt': 'O Pentecostes'},
            'description': {
                'it': 'Lo Spirito Santo scende su Maria e gli apostoli nel giorno di Pentecoste.',
                'en': 'The Holy Spirit descends upon Mary and the apostles on Pentecost.',
                'es': 'El Espíritu Santo desciende sobre María y los apóstoles en Pentecostés.',
                'pt': 'O Espírito Santo desce sobre Maria e os apóstolos no Pentecostes.'
            },
            'scripture_ref': 'Acts 2:1-13',
            'recommended_days': 'Wednesday, Sunday'
        },
        {
            'number': 4,
            'title': {'it': 'L\'Assunzione di Maria', 'en': 'The Assumption of Mary', 'es': 'La Asunción de María', 'pt': 'A Assunção de Maria'},
            'description': {
                'it': 'Maria è assunta in cielo in corpo e anima.',
                'en': 'Mary is assumed into heaven body and soul.',
                'es': 'María es asunta al cielo en cuerpo y alma.',
                'pt': 'Maria é assunta ao céu em corpo e alma.'
            },
            'scripture_ref': 'Revelation 12:1',
            'recommended_days': 'Wednesday, Sunday'
        },
        {
            'number': 5,
            'title': {'it': 'L\'Incoronazione di Maria', 'en': 'The Crowning of Mary', 'es': 'La Coronación de María', 'pt': 'A Coroação de Maria'},
            'description': {
                'it': 'Maria è incoronata Regina del Cielo e della terra nel Regno di Dio.',
                'en': 'Mary is crowned Queen of Heaven and earth in the Kingdom of God.',
                'es': 'María es coronada Reina del Cielo y de la tierra en el Reino de Dios.',
                'pt': 'Maria é coroada Rainha do Céu e da terra no Reino de Deus.'
            },
            'scripture_ref': 'Revelation 12:1-6',
            'recommended_days': 'Wednesday, Sunday'
        },
    ],
    'luminous': [
        {
            'number': 1,
            'title': {'it': 'Il Battesimo di Gesù', 'en': 'The Baptism of Jesus', 'es': 'El Bautismo de Jesús', 'pt': 'O Batismo de Jesus'},
            'description': {
                'it': 'Gesù è battezzato da Giovanni Battista nel fiume Giordano.',
                'en': 'Jesus is baptized by John the Baptist in the Jordan River.',
                'es': 'Jesús es bautizado por Juan Bautista en el río Jordán.',
                'pt': 'Jesus é batizado por João Batista no rio Jordão.'
            },
            'scripture_ref': 'Matthew 3:13-17',
            'recommended_days': 'Thursday'
        },
        {
            'number': 2,
            'title': {'it': 'Le Nozze di Cana', 'en': 'The Wedding at Cana', 'es': 'Las Bodas de Caná', 'pt': 'As Bodas de Caná'},
            'description': {
                'it': 'Gesù trasforma l\'acqua in vino alle nozze di Cana su intercessione di Maria.',
                'en': 'Jesus transforms water into wine at the wedding of Cana at Mary\'s intercession.',
                'es': 'Jesús transforma el agua en vino en las bodas de Caná por intercesión de María.',
                'pt': 'Jesus transforma água em vinho nas bodas de Caná pela intercessão de Maria.'
            },
            'scripture_ref': 'John 2:1-12',
            'recommended_days': 'Thursday'
        },
        {
            'number': 3,
            'title': {'it': 'L\'Annuncio del Regno', 'en': 'The Proclamation of the Kingdom', 'es': 'El Anuncio del Reino', 'pt': 'O Anúncio do Reino'},
            'description': {
                'it': 'Gesù predica il Vangelo e annuncia il Regno di Dio ai poveri e agli afflitti.',
                'en': 'Jesus preaches the Gospel and proclaims the Kingdom of God to the poor and afflicted.',
                'es': 'Jesús predica el Evangelio y anuncia el Reino de Dios a los pobres y afligidos.',
                'pt': 'Jesus prega o Evangelho e proclama o Reino de Deus aos pobres e aflitos.'
            },
            'scripture_ref': 'Mark 1:14-15',
            'recommended_days': 'Thursday'
        },
        {
            'number': 4,
            'title': {'it': 'La Trasfigurazione', 'en': 'The Transfiguration', 'es': 'La Transfiguración', 'pt': 'A Transfiguração'},
            'description': {
                'it': 'Gesù è trasfigurato sul monte Tabor davanti a Pietro, Giacomo e Giovanni.',
                'en': 'Jesus is transfigured on Mount Tabor before Peter, James, and John.',
                'es': 'Jesús es transfigurado en el monte Tabor ante Pedro, Santiago y Juan.',
                'pt': 'Jesus é transfigurado no monte Tabor diante de Pedro, Tiago e João.'
            },
            'scripture_ref': 'Matthew 17:1-8',
            'recommended_days': 'Thursday'
        },
        {
            'number': 5,
            'title': {'it': 'L\'Istituzione dell\'Eucaristia', 'en': 'The Institution of the Eucharist', 'es': 'La Institución de la Eucaristía', 'pt': 'A Instituição da Eucaristia'},
            'description': {
                'it': 'Gesù istituisce l\'Eucaristia e il sacerdozio nella Cena pasquale.',
                'en': 'Jesus institutes the Eucharist and the priesthood at the Last Supper.',
                'es': 'Jesús instituye la Eucaristía y el sacerdocio en la Última Cena.',
                'pt': 'Jesus institui a Eucaristia e o sacerdócio na Última Ceia.'
            },
            'scripture_ref': 'Matthew 26:26-29',
            'recommended_days': 'Thursday'
        },
    ]
}

def populate_rosary(db_path):
    """Insert all rosary mysteries into the rosary_mystery table"""
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    inserted = 0
    for mystery_type, mysteries in MYSTERIES.items():
        for mystery_data in mysteries:
            for lang in ['it', 'en', 'es', 'pt']:
                title = mystery_data['title'].get(lang, '')
                description = mystery_data['description'].get(lang, '')
                scripture_ref = mystery_data.get('scripture_ref', '')
                recommended_days = mystery_data.get('recommended_days', '')
                
                if title and description:
                    cur.execute("""
                        INSERT INTO rosary_mystery (type, number, lang, title, description, scripture_ref, recommended_days)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (mystery_type, mystery_data['number'], lang, title, description, scripture_ref, recommended_days))
                    inserted += 1
    
    conn.commit()
    conn.close()
    print(f"Populated {inserted} rosary mysteries")

if __name__ == '__main__':
    populate_rosary(DB_PATH)
