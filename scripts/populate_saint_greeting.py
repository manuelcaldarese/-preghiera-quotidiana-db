#!/usr/bin/env python3
"""
Populates saint_greeting table: short/long greeting and fun fact for main saints, 4 languages.
Static content.
"""

# Curated greetings for the most common saints.
# Format: saint_name → {lang: (greeting_short, greeting_long, fun_fact)}
SAINT_GREETINGS = {
    "Joseph": {
        "it": (
            "Buon onomastico! Oggi celebriamo San Giuseppe, sposo della Vergine Maria e padre putativo di Gesù.",
            "In questo giorno speciale vogliamo augurarti un felice onomastico. San Giuseppe è il patrono della Chiesa universale, dei lavoratori e delle famiglie. La sua vita ci insegna la fede silenziosa, l'obbedienza e la cura premurosa per chi amiamo. Che il suo esempio ti accompagni ogni giorno.",
            "San Giuseppe è il patrono di oltre 50 mestieri e professioni, tra cui falegnami, lavoratori, padri di famiglia e moribondi."
        ),
        "en": (
            "Happy feast day! Today we celebrate Saint Joseph, spouse of the Virgin Mary and foster father of Jesus.",
            "On this special day we wish you a happy name day. Saint Joseph is the patron of the universal Church, workers, and families. His life teaches us silent faith, obedience, and loving care for those we love. May his example guide you every day.",
            "Saint Joseph is the patron of over 50 trades and professions, including carpenters, workers, fathers, and the dying."
        ),
        "es": (
            "¡Feliz onomástica! Hoy celebramos a San José, esposo de la Virgen María y padre adoptivo de Jesús.",
            "En este día especial te deseamos un feliz onomástico. San José es el patrono de la Iglesia universal, de los trabajadores y de las familias. Su vida nos enseña la fe silenciosa, la obediencia y el cuidado amoroso por quienes amamos. Que su ejemplo te acompañe cada día.",
            "San José es patrono de más de 50 oficios y profesiones, entre ellos carpinteros, trabajadores, padres de familia y moribundos."
        ),
        "pt": (
            "Feliz onomástico! Hoje celebramos São José, esposo da Virgem Maria e pai adotivo de Jesus.",
            "Neste dia especial desejamos a você um feliz onomástico. São José é o patrono da Igreja universal, dos trabalhadores e das famílias. Sua vida nos ensina a fé silenciosa, a obediência e o cuidado amoroso por quem amamos. Que seu exemplo te acompanhe a cada dia.",
            "São José é patrono de mais de 50 ofícios e profissões, incluindo carpinteiros, trabalhadores, pais de família e moribundos."
        ),
    },
    "Mary, Mother of God": {
        "it": (
            "Buon onomastico! Oggi onoriamo Maria Santissima Madre di Dio, la più grande delle sante.",
            "Maria è il modello di ogni cristiano: fede totale, umiltà e amore senza confini. Il suo 'Eccomi' è il sì più bello della storia. Che la sua intercessione ti accompagni sempre.",
            "Il nome Maria è il nome femminile più diffuso al mondo in tutte le sue varianti linguistiche."
        ),
        "en": (
            "Happy feast day! Today we honor the Blessed Virgin Mary, Mother of God, the greatest of all saints.",
            "Mary is the model of every Christian: total faith, humility and boundless love. Her 'Fiat' is the most beautiful yes in history. May her intercession always be with you.",
            "The name Mary is the most widespread female name in the world across all its linguistic variants."
        ),
        "es": (
            "¡Feliz onomástica! Hoy honramos a la Santísima Virgen María, Madre de Dios, la más grande de todos los santos.",
            "María es el modelo de todo cristiano: fe total, humildad y amor sin límites. Su 'Fiat' es el sí más bello de la historia. Que su intercesión te acompañe siempre.",
            "El nombre María es el nombre femenino más extendido en el mundo en todas sus variantes lingüísticas."
        ),
        "pt": (
            "Feliz onomástico! Hoje honramos a Santíssima Virgem Maria, Mãe de Deus, a maior de todos os santos.",
            "Maria é o modelo de todo cristão: fé total, humildade e amor sem limites. O seu 'Fiat' é o sim mais belo da história. Que a sua intercessão te acompanhe sempre.",
            "O nome Maria é o nome feminino mais difundido no mundo em todas as suas variantes linguísticas."
        ),
    },
    "Anthony the Great": {
        "it": (
            "Buon onomastico! Oggi celebriamo Sant'Antonio Abate, padre del monachesimo cristiano.",
            "Sant'Antonio Abate visse per oltre cent'anni nel deserto egiziano, dedicando la sua vita alla preghiera e alla penitenza. È il patrono degli animali domestici e dei macellai. La sua forza spirituale è ancora oggi un faro per chi cerca Dio nel silenzio.",
            "Sant'Antonio è patrono degli animali domestici: il 17 gennaio in molte chiese si benedicono gli animali in suo onore."
        ),
        "en": (
            "Happy feast day! Today we celebrate Saint Anthony the Great, father of Christian monasticism.",
            "Saint Anthony the Great lived for over a hundred years in the Egyptian desert, dedicating his life to prayer and penance. He is the patron of domestic animals and butchers. His spiritual strength is still a beacon today for those who seek God in silence.",
            "Saint Anthony is patron of domestic animals: on January 17th in many churches animals are blessed in his honor."
        ),
        "es": (
            "¡Feliz onomástica! Hoy celebramos a San Antonio Abad, padre del monaquismo cristiano.",
            "San Antonio Abad vivió más de cien años en el desierto egipcio, dedicando su vida a la oración y la penitencia. Es patrono de los animales domésticos y de los carniceros. Su fortaleza espiritual sigue siendo hoy un faro para quienes buscan a Dios en el silencio.",
            "San Antonio es patrono de los animales domésticos: el 17 de enero en muchas iglesias se bendicen los animales en su honor."
        ),
        "pt": (
            "Feliz onomástico! Hoje celebramos Santo Antônio Abade, pai do monaquismo cristão.",
            "Santo Antônio Abade viveu mais de cem anos no deserto egípcio, dedicando sua vida à oração e à penitência. É patrono dos animais domésticos e dos açougueiros. Sua força espiritual ainda hoje é um farol para quem busca Deus no silêncio.",
            "Santo Antônio é patrono dos animais domésticos: no dia 17 de janeiro em muitas igrejas os animais são abençoados em sua honra."
        ),
    },
    "Anthony of Padua": {
        "it": (
            "Buon onomastico! Oggi celebriamo Sant'Antonio di Padova, il Santo dei miracoli e dei poveri.",
            "Sant'Antonio di Padova è uno dei santi più amati al mondo. Francescano e dottore della Chiesa, è invocato per ritrovare gli oggetti smarriti. La sua vita fu un continuo servizio ai poveri e agli ultimi. Porta il tuo nome con orgoglio!",
            "Sant'Antonio è il patrono dei poveri e degli oggetti smarriti. Morì a soli 35 anni ed è uno dei santi canonizzati più rapidamente della storia."
        ),
        "en": (
            "Happy feast day! Today we celebrate Saint Anthony of Padua, the Saint of miracles and the poor.",
            "Saint Anthony of Padua is one of the most beloved saints in the world. A Franciscan and Doctor of the Church, he is invoked to find lost objects. His life was a continuous service to the poor and marginalized. Wear your name with pride!",
            "Saint Anthony is the patron of the poor and lost objects. He died at only 35 years old and is one of the most quickly canonized saints in history."
        ),
        "es": (
            "¡Feliz onomástica! Hoy celebramos a San Antonio de Padua, el Santo de los milagros y de los pobres.",
            "San Antonio de Padua es uno de los santos más queridos del mundo. Franciscano y Doctor de la Iglesia, es invocado para encontrar los objetos perdidos. Su vida fue un continuo servicio a los pobres y marginados. ¡Lleva tu nombre con orgullo!",
            "San Antonio es patrono de los pobres y de los objetos perdidos. Murió con solo 35 años y es uno de los santos canonizados más rápidamente de la historia."
        ),
        "pt": (
            "Feliz onomástico! Hoje celebramos Santo Antônio de Pádua, o Santo dos milagres e dos pobres.",
            "Santo Antônio de Pádua é um dos santos mais amados do mundo. Franciscano e Doutor da Igreja, é invocado para encontrar objetos perdidos. Sua vida foi um serviço contínuo aos pobres e marginalizados. Use seu nome com orgulho!",
            "Santo Antônio é patrono dos pobres e dos objetos perdidos. Morreu com apenas 35 anos e é um dos santos canonizados mais rapidamente da história."
        ),
    },
    "John the Baptist": {
        "it": (
            "Buon onomastico! Oggi celebriamo la Natività di San Giovanni Battista, il precursore di Cristo.",
            "San Giovanni Battista è l'unico santo oltre la Vergine Maria di cui celebriamo la nascita (non la morte). La sua voce nel deserto ancora oggi chiama alla conversione e alla speranza. 'Preparate la via del Signore!'",
            "San Giovanni Battista è uno dei santi più citati nel Vangelo. La sua festa è il 24 giugno, esattamente 6 mesi prima del Natale."
        ),
        "en": (
            "Happy feast day! Today we celebrate the Birth of Saint John the Baptist, the forerunner of Christ.",
            "Saint John the Baptist is the only saint besides the Virgin Mary whose birth we celebrate (not death). His voice in the desert still calls to conversion and hope today. 'Prepare the way of the Lord!'",
            "Saint John the Baptist is one of the most quoted saints in the Gospel. His feast is June 24th, exactly 6 months before Christmas."
        ),
        "es": (
            "¡Feliz onomástica! Hoy celebramos el Nacimiento de San Juan Bautista, el precursor de Cristo.",
            "San Juan Bautista es el único santo además de la Virgen María cuyo nacimiento celebramos (no su muerte). Su voz en el desierto todavía hoy llama a la conversión y a la esperanza. '¡Preparad el camino del Señor!'",
            "San Juan Bautista es uno de los santos más citados en el Evangelio. Su fiesta es el 24 de junio, exactamente 6 meses antes de Navidad."
        ),
        "pt": (
            "Feliz onomástico! Hoje celebramos o Nascimento de São João Batista, o precursor de Cristo.",
            "São João Batista é o único santo além da Virgem Maria cujo nascimento celebramos (não a morte). Sua voz no deserto ainda hoje chama à conversão e à esperança. 'Preparai o caminho do Senhor!'",
            "São João Batista é um dos santos mais citados no Evangelho. Sua festa é 24 de junho, exatamente 6 meses antes do Natal."
        ),
    },
    "Peter the Apostle": {
        "it": (
            "Buon onomastico! Oggi celebriamo San Pietro Apostolo, la roccia su cui Cristo ha edificato la sua Chiesa.",
            "San Pietro, pescatore di Galilea, divenne il primo Papa e il fondamento visibile della Chiesa. Nonostante le sue debolezze — la triplice negazione — fu scelto da Gesù per guidare il gregge. Un esempio di misericordia e di seconda possibilità.",
            "La tomba di San Pietro si trova sotto l'altare maggiore della Basilica di San Pietro in Vaticano."
        ),
        "en": (
            "Happy feast day! Today we celebrate Saint Peter the Apostle, the rock upon which Christ built His Church.",
            "Saint Peter, a fisherman from Galilee, became the first Pope and the visible foundation of the Church. Despite his weaknesses — the threefold denial — he was chosen by Jesus to lead the flock. An example of mercy and second chances.",
            "Saint Peter's tomb is located beneath the main altar of St. Peter's Basilica in the Vatican."
        ),
        "es": (
            "¡Feliz onomástica! Hoy celebramos a San Pedro Apóstol, la roca sobre la que Cristo edificó su Iglesia.",
            "San Pedro, pescador de Galilea, se convirtió en el primer Papa y en el fundamento visible de la Iglesia. A pesar de sus debilidades — la triple negación — fue elegido por Jesús para guiar al rebaño. Un ejemplo de misericordia y de segunda oportunidad.",
            "La tumba de San Pedro se encuentra bajo el altar mayor de la Basílica de San Pedro en el Vaticano."
        ),
        "pt": (
            "Feliz onomástico! Hoje celebramos São Pedro Apóstolo, a pedra sobre a qual Cristo edificou sua Igreja.",
            "São Pedro, pescador da Galileia, tornou-se o primeiro Papa e o fundamento visível da Igreja. Apesar de suas fraquezas — a tríplice negação — foi escolhido por Jesus para guiar o rebanho. Um exemplo de misericórdia e de segunda chance.",
            "O túmulo de São Pedro está localizado sob o altar-mor da Basílica de São Pedro no Vaticano."
        ),
    },
    "Paul the Apostle": {
        "it": (
            "Buon onomastico! Oggi celebriamo San Paolo Apostolo, il grande missionario che ha portato il Vangelo al mondo.",
            "San Paolo, da persecutore dei cristiani a instancabile apostolo, è l'esempio più straordinario della grazia di Dio. Le sue lettere sono ancora oggi guida spirituale per milioni di credenti.",
            "San Paolo ha percorso circa 15.000 km nei suoi viaggi missionari — più di qualsiasi altro apostolo."
        ),
        "en": (
            "Happy feast day! Today we celebrate Saint Paul the Apostle, the great missionary who brought the Gospel to the world.",
            "Saint Paul, from persecutor of Christians to tireless apostle, is the most extraordinary example of God's grace. His letters are still today a spiritual guide for millions of believers.",
            "Saint Paul traveled approximately 15,000 km on his missionary journeys — more than any other apostle."
        ),
        "es": (
            "¡Feliz onomástica! Hoy celebramos a San Pablo Apóstol, el gran misionero que llevó el Evangelio al mundo.",
            "San Pablo, de perseguidor de los cristianos a incansable apóstol, es el ejemplo más extraordinario de la gracia de Dios. Sus cartas son todavía hoy guía espiritual para millones de creyentes.",
            "San Pablo recorrió aproximadamente 15.000 km en sus viajes misioneros, más que cualquier otro apóstol."
        ),
        "pt": (
            "Feliz onomástico! Hoje celebramos São Paulo Apóstolo, o grande missionário que levou o Evangelho ao mundo.",
            "São Paulo, de perseguidor dos cristãos a incansável apóstolo, é o exemplo mais extraordinário da graça de Deus. Suas cartas ainda hoje são guia espiritual para milhões de crentes.",
            "São Paulo percorreu aproximadamente 15.000 km em suas viagens missionárias — mais do que qualquer outro apóstolo."
        ),
    },
    "Francis of Assisi": {
        "it": (
            "Buon onomastico! Oggi celebriamo San Francesco d'Assisi, il poverello di Assisi amato in tutto il mondo.",
            "San Francesco d'Assisi scelse la povertà radicale e il servizio ai lebbrosi, fondando uno degli ordini religiosi più diffusi al mondo. Il suo Cantico delle Creature è la prima poesia della letteratura italiana.",
            "San Francesco è il patrono d'Italia e patrono degli ecologisti. Il suo nome è stato scelto da Papa Francesco nel 2013."
        ),
        "en": (
            "Happy feast day! Today we celebrate Saint Francis of Assisi, the little poor man of Assisi, beloved throughout the world.",
            "Saint Francis of Assisi chose radical poverty and service to lepers, founding one of the most widespread religious orders in the world. His Canticle of the Creatures is the first poem of Italian literature.",
            "Saint Francis is the patron of Italy and patron of ecologists. His name was chosen by Pope Francis in 2013."
        ),
        "es": (
            "¡Feliz onomástica! Hoy celebramos a San Francisco de Asís, el pobrecillo de Asís amado en todo el mundo.",
            "San Francisco de Asís eligió la pobreza radical y el servicio a los leprosos, fundando una de las órdenes religiosas más extendidas del mundo. Su Cántico de las Criaturas es el primer poema de la literatura italiana.",
            "San Francisco es patrono de Italia y patrono de los ecologistas. Su nombre fue elegido por el Papa Francisco en 2013."
        ),
        "pt": (
            "Feliz onomástico! Hoje celebramos São Francisco de Assis, o pobrezinho de Assis amado em todo o mundo.",
            "São Francisco de Assis escolheu a pobreza radical e o serviço aos leprosos, fundando uma das ordens religiosas mais difundidas do mundo. Seu Cântico das Criaturas é o primeiro poema da literatura italiana.",
            "São Francisco é patrono da Itália e patrono dos ecologistas. Seu nome foi escolhido pelo Papa Francisco em 2013."
        ),
    },
    "Thomas Aquinas": {
        "it": (
            "Buon onomastico! Oggi celebriamo San Tommaso d'Aquino, il Dottore Angelico, principe della teologia cattolica.",
            "San Tommaso d'Aquino fu il più grande teologo e filosofo del Medioevo. La sua Summa Theologiae è ancora oggi il punto di riferimento della teologia cattolica. Patrono degli studenti e delle università.",
            "San Tommaso scrisse la Summa Theologiae a soli 47 anni, uno dei testi filosofici più influenti della storia."
        ),
        "en": (
            "Happy feast day! Today we celebrate Saint Thomas Aquinas, the Angelic Doctor, prince of Catholic theology.",
            "Saint Thomas Aquinas was the greatest theologian and philosopher of the Middle Ages. His Summa Theologiae is still today the point of reference for Catholic theology. Patron of students and universities.",
            "Saint Thomas wrote the Summa Theologiae at only 47 years old, one of the most influential philosophical texts in history."
        ),
        "es": (
            "¡Feliz onomástica! Hoy celebramos a Santo Tomás de Aquino, el Doctor Angélico, príncipe de la teología católica.",
            "Santo Tomás de Aquino fue el mayor teólogo y filósofo de la Edad Media. Su Suma Teológica es todavía hoy el punto de referencia de la teología católica. Patrono de los estudiantes y de las universidades.",
            "Santo Tomás escribió la Suma Teológica con solo 47 años, uno de los textos filosóficos más influyentes de la historia."
        ),
        "pt": (
            "Feliz onomástico! Hoje celebramos São Tomás de Aquino, o Doutor Angélico, príncipe da teologia católica.",
            "São Tomás de Aquino foi o maior teólogo e filósofo da Idade Média. Sua Suma Teológica ainda hoje é o ponto de referência da teologia católica. Patrono dos estudantes e das universidades.",
            "São Tomás escreveu a Suma Teológica com apenas 47 anos, um dos textos filosóficos mais influentes da história."
        ),
    },
    "Teresa of Ávila": {
        "it": (
            "Buon onomastico! Oggi celebriamo Santa Teresa d'Avila, mistica e Dottore della Chiesa.",
            "Santa Teresa d'Avila fu una delle grandi mistiche della storia cristiana e riformatrice dell'Ordine Carmelitano. I suoi scritti, come il Cammino di Perfezione, guidano ancora oggi chi cerca Dio nell'orazione.",
            "Santa Teresa fu la prima donna proclamata Dottore della Chiesa, insieme a Santa Caterina da Siena, nel 1970."
        ),
        "en": (
            "Happy feast day! Today we celebrate Saint Teresa of Ávila, mystic and Doctor of the Church.",
            "Saint Teresa of Ávila was one of the great mystics of Christian history and reformer of the Carmelite Order. Her writings, such as The Way of Perfection, still guide those who seek God in prayer.",
            "Saint Teresa was the first woman proclaimed Doctor of the Church, together with Saint Catherine of Siena, in 1970."
        ),
        "es": (
            "¡Feliz onomástica! Hoy celebramos a Santa Teresa de Ávila, mística y Doctora de la Iglesia.",
            "Santa Teresa de Ávila fue una de las grandes místicas de la historia cristiana y reformadora de la Orden Carmelita. Sus escritos, como el Camino de Perfección, todavía hoy guían a quienes buscan a Dios en la oración.",
            "Santa Teresa fue la primera mujer proclamada Doctora de la Iglesia, junto con Santa Catalina de Siena, en 1970."
        ),
        "pt": (
            "Feliz onomástico! Hoje celebramos Santa Teresa de Ávila, mística e Doutora da Igreja.",
            "Santa Teresa de Ávila foi uma das grandes místicas da história cristã e reformadora da Ordem Carmelita. Seus escritos, como o Caminho de Perfeição, ainda hoje guiam quem busca Deus na oração.",
            "Santa Teresa foi a primeira mulher proclamada Doutora da Igreja, juntamente com Santa Catarina de Siena, em 1970."
        ),
    },
}

# Generic template for saints not in the curated list
GENERIC_TEMPLATES = {
    "it": (
        "Buon onomastico! Oggi la Chiesa celebra {saint_name}. Che questo giorno sia per te fonte di gioia e benedizione.",
        "Nel giorno del tuo onomastico vogliamo augurarti ogni bene. {saint_name} è un esempio di fede e dedizione a Dio. Porta il tuo nome con orgoglio e lasciati ispirare dalla sua vita.",
        None
    ),
    "en": (
        "Happy feast day! Today the Church celebrates {saint_name}. May this day be a source of joy and blessing for you.",
        "On your name day we wish you every blessing. {saint_name} is an example of faith and dedication to God. Wear your name with pride and let their life inspire you.",
        None
    ),
    "es": (
        "¡Feliz onomástica! Hoy la Iglesia celebra a {saint_name}. Que este día sea para ti fuente de alegría y bendición.",
        "En el día de tu onomástico te deseamos todo bien. {saint_name} es un ejemplo de fe y dedicación a Dios. Lleva tu nombre con orgullo y déjate inspirar por su vida.",
        None
    ),
    "pt": (
        "Feliz onomástico! Hoje a Igreja celebra {saint_name}. Que este dia seja para você fonte de alegria e bênção.",
        "No dia do seu onomástico desejamos a você toda a bênção. {saint_name} é um exemplo de fé e dedicação a Deus. Use seu nome com orgulho e deixe-se inspirar pela sua vida.",
        None
    ),
}

# All saint names from feast_calendar that should have greetings
ALL_SAINT_NAMES = [
    "Mary, Mother of God", "Basil and Gregory", "Genevieve", "Raymond of Penyafort",
    "Hilary of Poitiers", "Anthony the Great", "Fabian", "Sebastian", "Agnes of Rome",
    "Vincent of Saragossa", "Francis de Sales", "Timothy and Titus", "Angela Merici",
    "Thomas Aquinas", "John Bosco", "Blaise of Sebaste", "Agatha of Sicily",
    "Paul Miki", "Scholastica", "Our Lady of Lourdes", "Cyril and Methodius",
    "Patrick of Ireland", "Joseph", "Francis of Assisi", "Anthony of Padua",
    "Dominic", "Lawrence of Rome", "Clare of Assisi", "Maximilian Kolbe",
    "Bernard of Clairvaux", "Monica", "Augustine of Hippo", "Gregory the Great",
    "Peter Claver", "John Chrysostom", "Robert Bellarmine", "Jerome",
    "Thérèse of Lisieux", "Guardian Angels", "Teresa of Ávila", "Luke the Evangelist",
    "Andrew", "Francis Xavier", "Nicholas of Myra", "Ambrose", "Lucy of Syracuse",
    "John of the Cross", "Stephen the first martyr", "John the Apostle",
    "Sylvester I", "John the Baptist", "Peter the Apostle", "Paul the Apostle",
    "Mary Magdalene", "Bridget of Sweden", "James the Apostle", "Martha",
    "Ignatius of Loyola", "John Vianney", "Bartholomew", "Louis IX of France",
    "Cecilia", "Charles Borromeo", "Martin of Tours", "Elizabeth of Hungary",
    "Joachim and Anne", "Thomas the Apostle", "Michael, Gabriel, Raphael",
    "Catherine of Siena", "George", "Mark the Evangelist", "Matthew",
    "Peter and Paul", "Padre Pio", "Philip and James", "Matthias",
    "Cosmas and Damian", "Lawrence of Brindisi", "Alphonsus Liguori",
    "Jane Frances de Chantal", "Pontian and Hippolytus", "Assumption of Mary",
    "Pius X", "Queenship of Mary", "Beheading of John the Baptist",
    "Birth of Mary", "Our Lady of Sorrows", "Cornelius and Cyprian",
    "Januarius", "Wenceslaus", "Vincent de Paul", "Cosmas and Damian",
    "Denis of Paris", "Callixtus I", "Hedwig of Silesia", "Margaret Mary Alacoque",
    "Ignatius of Antioch", "Jean de Brébeuf", "John Paul II", "Simon and Jude",
    "Martin de Porres", "Leo the Great", "Josaphat", "Albert the Great",
    "Presentation of Mary", "Clement I", "Immaculate Conception", "Juan Diego",
    "Our Lady of Guadalupe", "Peter Canisius", "Thomas Becket",
    "Holy Innocents", "Fabian", "Anselm of Canterbury", "Fidelis of Sigmaringen",
    "Peter Chanel", "Philip Neri", "Bede the Venerable", "Gregory VII",
    "Barnabas", "Romuald", "Aloysius Gonzaga", "Paulinus of Nola",
    "John Fisher", "Thomas More", "Irenaeus", "Charbel Makhlouf",
    "Peter Chrysologus", "Alphonsus Liguori", "Sixtus II", "Henry",
    "Apollinaris", "Bonaventure", "Our Lady of Mount Carmel",
    "John Vianney", "Transfiguration", "Clare of Assisi",
    "Maximilian Kolbe", "Pius X", "Bartholomew", "Monica",
    "Beheading of John the Baptist", "Gregory the Great", "Peter Claver",
    "Exaltation of the Cross", "Robert Bellarmine", "Januarius",
    "Padre Pio", "Wenceslaus", "Jerome", "Bruno of Cologne",
    "Hedwig of Silesia", "Ignatius of Antioch", "Luke the Evangelist",
    "Anthony Mary Claret", "Stanislaus",
]


def get_saint_greeting_rows() -> list[tuple]:
    rows = []
    seen = set()
    for saint_name in ALL_SAINT_NAMES:
        if saint_name in seen:
            continue
        seen.add(saint_name)
        for lang in ['it', 'en', 'es', 'pt']:
            if saint_name in SAINT_GREETINGS and lang in SAINT_GREETINGS[saint_name]:
                short, long_, fun = SAINT_GREETINGS[saint_name][lang]
            else:
                tmpl = GENERIC_TEMPLATES[lang]
                short = tmpl[0].format(saint_name=saint_name)
                long_ = tmpl[1].format(saint_name=saint_name)
                fun = tmpl[2]
            rows.append((saint_name, lang, short, long_, fun))
    return rows


if __name__ == '__main__':
    rows = get_saint_greeting_rows()
    print(f"saint_greeting: {len(rows)} righe")
    for r in rows[:4]:
        print(r[0], r[1], r[2][:60])
