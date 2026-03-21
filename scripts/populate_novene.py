#!/usr/bin/env python3
"""
Novene — 5 novene × 9 giorni × 4 lingue = 180 righe
Testi tradizionali cattolici.
"""

NOVENE = {

    # -------------------------------------------------------------------------
    'christmas': {
        'title': {
            'it': 'Novena di Natale',
            'en': 'Christmas Novena',
            'es': 'Novena de Navidad',
            'pt': 'Novena de Natal',
        },
        'days': [
            {
                'intention': {
                    'it': 'Prepara il tuo cuore all\'arrivo del Salvatore',
                    'en': 'Prepare your heart for the coming of the Saviour',
                    'es': 'Prepara tu corazón para la venida del Salvador',
                    'pt': 'Prepara o teu coração para a vinda do Salvador',
                },
                'scripture_ref': 'Is 7,14',
                'prayer': {
                    'it': 'O Gesù, che stai per venire nel mondo, vieni anche nel mio cuore. Preparami ad accoglierti con fede e amore. Libera il mio cuore da tutto ciò che ti impedisce di entrare. Amen.',
                    'en': 'O Jesus, who is about to come into the world, come also into my heart. Prepare me to welcome you with faith and love. Free my heart from all that keeps you from entering. Amen.',
                    'es': 'Oh Jesús, que estás a punto de venir al mundo, ven también a mi corazón. Prepárame para acogerte con fe y amor. Libera mi corazón de todo lo que te impide entrar. Amén.',
                    'pt': 'Ó Jesus, que estás prestes a vir ao mundo, vem também ao meu coração. Prepara-me para te acolher com fé e amor. Liberta o meu coração de tudo o que te impede de entrar. Amém.',
                },
            },
            {
                'intention': {
                    'it': 'Per la pace nel mondo e nelle famiglie',
                    'en': 'For peace in the world and in families',
                    'es': 'Por la paz en el mundo y en las familias',
                    'pt': 'Pela paz no mundo e nas famílias',
                },
                'scripture_ref': 'Is 9,5',
                'prayer': {
                    'it': 'O Principe della Pace, vieni a portare la tua pace nel mondo. Guarisci le divisioni tra i popoli e le ferite nelle famiglie. Che il tuo Natale porti riconciliazione e amore. Amen.',
                    'en': 'O Prince of Peace, come to bring your peace to the world. Heal divisions among peoples and wounds within families. May your Christmas bring reconciliation and love. Amen.',
                    'es': 'Oh Príncipe de la Paz, ven a traer tu paz al mundo. Sana las divisiones entre los pueblos y las heridas en las familias. Que tu Navidad traiga reconciliación y amor. Amén.',
                    'pt': 'Ó Príncipe da Paz, vem trazer a tua paz ao mundo. Cura as divisões entre os povos e as feridas nas famílias. Que o teu Natal traga reconciliação e amor. Amém.',
                },
            },
            {
                'intention': {
                    'it': 'Per i poveri e i senza casa',
                    'en': 'For the poor and the homeless',
                    'es': 'Por los pobres y los sin hogar',
                    'pt': 'Pelos pobres e pelos sem-teto',
                },
                'scripture_ref': 'Lc 2,7',
                'prayer': {
                    'it': 'O Gesù, nato in una stalla perché non c\'era posto per te, guarda i fratelli e le sorelle che oggi non hanno un tetto. Accendi nei nostri cuori il fuoco della carità verso chi è nel bisogno. Amen.',
                    'en': 'O Jesus, born in a stable because there was no room for you, look upon the brothers and sisters who today have no roof over their heads. Kindle in our hearts the fire of charity toward those in need. Amen.',
                    'es': 'Oh Jesús, nacido en un establo porque no había lugar para ti, mira a los hermanos y hermanas que hoy no tienen techo. Enciende en nuestros corazones el fuego de la caridad hacia los que están en necesidad. Amén.',
                    'pt': 'Ó Jesus, nascido num estábulo porque não havia lugar para ti, olha para os irmãos e irmãs que hoje não têm teto. Acende em nossos corações o fogo da caridade para com os necessitados. Amém.',
                },
            },
            {
                'intention': {
                    'it': 'Per i bambini del mondo',
                    'en': 'For the children of the world',
                    'es': 'Por los niños del mundo',
                    'pt': 'Pelas crianças do mundo',
                },
                'scripture_ref': 'Mt 18,3',
                'prayer': {
                    'it': 'O Gesù Bambino, tu hai voluto essere piccolo come i bambini. Proteggi tutti i bambini del mondo, specialmente quelli che soffrono. Fa\' che ogni bambino conosca l\'amore e la gioia del tuo Natale. Amen.',
                    'en': 'O Child Jesus, you chose to become small like children. Protect all the children of the world, especially those who suffer. May every child know the love and joy of your Christmas. Amen.',
                    'es': 'Oh Niño Jesús, quisiste ser pequeño como los niños. Protege a todos los niños del mundo, especialmente a los que sufren. Haz que cada niño conozca el amor y la alegría de tu Navidad. Amén.',
                    'pt': 'Ó Menino Jesus, quiseste ser pequeno como as crianças. Protege todas as crianças do mundo, especialmente as que sofrem. Faz que cada criança conheça o amor e a alegria do teu Natal. Amém.',
                },
            },
            {
                'intention': {
                    'it': 'Per i lontani dalla fede',
                    'en': 'For those far from the faith',
                    'es': 'Por los alejados de la fe',
                    'pt': 'Pelos afastados da fé',
                },
                'scripture_ref': 'Lc 2,10',
                'prayer': {
                    'it': 'O Gesù, luce del mondo, illumina coloro che camminano nelle tenebre lontani da te. Che la gioia del Natale tocchi il loro cuore e li riporti a te. Amen.',
                    'en': 'O Jesus, light of the world, enlighten those who walk in darkness far from you. May the joy of Christmas touch their hearts and bring them back to you. Amen.',
                    'es': 'Oh Jesús, luz del mundo, ilumina a quienes caminan en las tinieblas lejos de ti. Que la alegría de la Navidad toque su corazón y los devuelva a ti. Amén.',
                    'pt': 'Ó Jesus, luz do mundo, ilumina aqueles que caminham nas trevas longe de ti. Que a alegria do Natal toque o seu coração e os traga de volta a ti. Amém.',
                },
            },
            {
                'intention': {
                    'it': 'Per i malati e chi li assiste',
                    'en': 'For the sick and those who care for them',
                    'es': 'Por los enfermos y quienes los cuidan',
                    'pt': 'Pelos doentes e quem os assiste',
                },
                'scripture_ref': 'Is 53,4',
                'prayer': {
                    'it': 'O Gesù, tu hai portato le nostre infermità. Conforta i malati in questo tempo di Natale. Sostieni chi li assiste con pazienza e dedizione. Che nessuno trascorra le feste nella solitudine e nel dolore. Amen.',
                    'en': 'O Jesus, you have borne our infirmities. Comfort the sick in this Christmas season. Sustain those who care for them with patience and dedication. May no one spend the holidays in loneliness and pain. Amen.',
                    'es': 'Oh Jesús, tú has llevado nuestras enfermedades. Conforta a los enfermos en este tiempo de Navidad. Sostén a quienes los cuidan con paciencia y dedicación. Que nadie pase las fiestas en la soledad y el dolor. Amén.',
                    'pt': 'Ó Jesus, tu carregaste as nossas enfermidades. Conforta os doentes neste tempo de Natal. Sustenta quem os assiste com paciência e dedicação. Que ninguém passe as festas na solidão e na dor. Amém.',
                },
            },
            {
                'intention': {
                    'it': 'Per la nostra famiglia',
                    'en': 'For our family',
                    'es': 'Por nuestra familia',
                    'pt': 'Pela nossa família',
                },
                'scripture_ref': 'Lc 2,51',
                'prayer': {
                    'it': 'O Gesù, che hai voluto nascere in una famiglia, benedici la nostra. Uniscila nell\'amore, proteggila dal male, guidala verso di te. Fa\' che il nostro focolare sia un riflesso della casa di Nazareth. Amen.',
                    'en': 'O Jesus, who chose to be born into a family, bless ours. Unite it in love, protect it from evil, guide it toward you. May our home be a reflection of the house of Nazareth. Amen.',
                    'es': 'Oh Jesús, que quisiste nacer en una familia, bendice la nuestra. Únela en el amor, protégela del mal, guíala hacia ti. Haz que nuestro hogar sea un reflejo de la casa de Nazaret. Amén.',
                    'pt': 'Ó Jesus, que quiseste nascer numa família, abençoa a nossa. Una-a no amor, protege-a do mal, guia-a para ti. Faz que o nosso lar seja um reflexo da casa de Nazaré. Amém.',
                },
            },
            {
                'intention': {
                    'it': 'Ringraziamento per i doni ricevuti',
                    'en': 'Thanksgiving for gifts received',
                    'es': 'Acción de gracias por los dones recibidos',
                    'pt': 'Ação de graças pelos dons recebidos',
                },
                'scripture_ref': 'Gv 3,16',
                'prayer': {
                    'it': 'Padre, ti ringraziamo per il dono inestimabile di tuo Figlio. Ogni bene nella nostra vita viene da te. Insegnaci a riconoscere i tuoi doni e a usarli per gli altri. Amen.',
                    'en': 'Father, we thank you for the inestimable gift of your Son. Every good in our life comes from you. Teach us to recognize your gifts and to use them for others. Amen.',
                    'es': 'Padre, te damos gracias por el don inestimable de tu Hijo. Todo bien en nuestra vida viene de ti. Enséñanos a reconocer tus dones y a utilizarlos para los demás. Amén.',
                    'pt': 'Pai, agradecemos-te pelo dom inestimável do teu Filho. Todo bem em nossa vida vem de ti. Ensina-nos a reconhecer os teus dons e a usá-los para os outros. Amém.',
                },
            },
            {
                'intention': {
                    'it': 'Offerta di sé per il nuovo anno',
                    'en': 'Offering of self for the new year',
                    'es': 'Ofrenda de uno mismo para el nuevo año',
                    'pt': 'Oferta de si mesmo para o novo ano',
                },
                'scripture_ref': 'Rm 12,1',
                'prayer': {
                    'it': 'O Gesù, nel giorno del tuo Natale mi offro a te. Prendi la mia vita, i miei progetti, i miei sogni. Guidami nel nuovo anno secondo la tua volontà. Fa\' di me quello che vuoi, purché io sia tuo. Amen.',
                    'en': 'O Jesus, on the day of your Nativity I offer myself to you. Take my life, my plans, my dreams. Guide me in the new year according to your will. Make of me what you will, as long as I am yours. Amen.',
                    'es': 'Oh Jesús, en el día de tu Navidad me ofrezco a ti. Toma mi vida, mis proyectos, mis sueños. Guíame en el nuevo año según tu voluntad. Haz de mí lo que quieras, con tal de que sea tuyo. Amén.',
                    'pt': 'Ó Jesus, no dia do teu Natal ofereço-me a ti. Toma a minha vida, os meus projetos, os meus sonhos. Guia-me no novo ano segundo a tua vontade. Faz de mim o que quiseres, contanto que eu seja teu. Amém.',
                },
            },
        ],
    },

    # -------------------------------------------------------------------------
    'saint_joseph': {
        'title': {
            'it': 'Novena a San Giuseppe',
            'en': 'Novena to Saint Joseph',
            'es': 'Novena a San José',
            'pt': 'Novena a São José',
        },
        'days': [
            {
                'intention': {
                    'it': 'Per la protezione delle famiglie',
                    'en': 'For the protection of families',
                    'es': 'Por la protección de las familias',
                    'pt': 'Pela proteção das famílias',
                },
                'scripture_ref': 'Mt 1,20',
                'prayer': {
                    'it': 'O San Giuseppe, custode della Sacra Famiglia, proteggi la mia famiglia. Intercedi per noi affinché ogni casa sia fondata sull\'amore di Dio. Amen.',
                    'en': 'O Saint Joseph, guardian of the Holy Family, protect my family. Intercede for us that every home may be founded on the love of God. Amen.',
                    'es': 'Oh San José, custodio de la Sagrada Familia, protege mi familia. Intercede por nosotros para que cada hogar esté fundado en el amor de Dios. Amén.',
                    'pt': 'Ó São José, guardião da Sagrada Família, protege a minha família. Intercede por nós para que cada lar seja fundado no amor de Deus. Amém.',
                },
            },
            {
                'intention': {
                    'it': 'Per i lavoratori e i disoccupati',
                    'en': 'For workers and the unemployed',
                    'es': 'Por los trabajadores y los desempleados',
                    'pt': 'Pelos trabalhadores e desempregados',
                },
                'scripture_ref': 'Mt 13,55',
                'prayer': {
                    'it': 'O San Giuseppe, artigiano e lavoratore, benedici il lavoro delle nostre mani. Conforta chi ha perso il lavoro e aiutalo a trovare una nuova via. Amen.',
                    'en': 'O Saint Joseph, craftsman and worker, bless the work of our hands. Comfort those who have lost their jobs and help them find a new path. Amen.',
                    'es': 'Oh San José, artesano y trabajador, bendice el trabajo de nuestras manos. Conforta a los que han perdido su trabajo y ayúdalos a encontrar un nuevo camino. Amén.',
                    'pt': 'Ó São José, artesão e trabalhador, abençoa o trabalho das nossas mãos. Conforta quem perdeu o emprego e ajuda-o a encontrar um novo caminho. Amém.',
                },
            },
            {
                'intention': {
                    'it': 'Per i padri di famiglia',
                    'en': 'For fathers and heads of families',
                    'es': 'Por los padres de familia',
                    'pt': 'Pelos pais de família',
                },
                'scripture_ref': 'Lc 2,48',
                'prayer': {
                    'it': 'O Giuseppe, padre giusto e amorevole, intercedi per tutti i padri. Donali saggezza, pazienza e la forza di guidare le loro famiglie verso Dio. Amen.',
                    'en': 'O Joseph, just and loving father, intercede for all fathers. Grant them wisdom, patience, and the strength to guide their families toward God. Amen.',
                    'es': 'Oh José, padre justo y amoroso, intercede por todos los padres. Concédeles sabiduría, paciencia y la fuerza para guiar a sus familias hacia Dios. Amén.',
                    'pt': 'Ó José, pai justo e amoroso, intercede por todos os pais. Concede-lhes sabedoria, paciência e a força para guiar as suas famílias em direção a Deus. Amém.',
                },
            },
            {
                'intention': {
                    'it': 'Per chi attraversa l\'oscurità e il dubbio',
                    'en': 'For those passing through darkness and doubt',
                    'es': 'Por los que atraviesan la oscuridad y la duda',
                    'pt': 'Por quem atravessa a escuridão e a dúvida',
                },
                'scripture_ref': 'Mt 1,24',
                'prayer': {
                    'it': 'O Giuseppe, che hai obbedito a Dio anche nell\'incomprensibile, aiuta chi non riesce a comprendere i disegni di Dio. Insegnaci a fidarci nel buio. Amen.',
                    'en': 'O Joseph, who obeyed God even in the incomprehensible, help those who cannot understand God\'s plans. Teach us to trust in the dark. Amen.',
                    'es': 'Oh José, que obedeciste a Dios incluso en lo incomprensible, ayuda a quienes no pueden comprender los designios de Dios. Enséñanos a confiar en la oscuridad. Amén.',
                    'pt': 'Ó José, que obedeceste a Deus mesmo no incompreensível, ajuda quem não consegue compreender os desígnios de Deus. Ensina-nos a confiar na escuridão. Amém.',
                },
            },
            {
                'intention': {
                    'it': 'Per la Chiesa universale',
                    'en': 'For the universal Church',
                    'es': 'Por la Iglesia universal',
                    'pt': 'Pela Igreja universal',
                },
                'scripture_ref': 'Ef 5,25',
                'prayer': {
                    'it': 'O San Giuseppe, patrono della Chiesa universale, proteggila dagli attacchi del maligno. Guida Papa, vescovi e sacerdoti nell\'amore fedele allo Sposo divino. Amen.',
                    'en': 'O Saint Joseph, patron of the universal Church, protect her from the attacks of the evil one. Guide the Pope, bishops, and priests in faithful love for the divine Bridegroom. Amen.',
                    'es': 'Oh San José, patrón de la Iglesia universal, protégela de los ataques del maligno. Guía al Papa, obispos y sacerdotes en el amor fiel al Esposo divino. Amén.',
                    'pt': 'Ó São José, patrono da Igreja universal, protege-a dos ataques do maligno. Guia o Papa, bispos e sacerdotes no amor fiel ao Esposo divino. Amém.',
                },
            },
            {
                'intention': {
                    'it': 'Per i moribondi e per una buona morte',
                    'en': 'For the dying and for a good death',
                    'es': 'Por los moribundos y por una buena muerte',
                    'pt': 'Pelos moribundos e por uma boa morte',
                },
                'scripture_ref': 'Sal 23,4',
                'prayer': {
                    'it': 'O San Giuseppe, patrono dei moribondi, assistimi nell\'ora della mia morte. Intercedi perché possa spirare tra le braccia di Gesù e Maria, come è accaduto a te. Amen.',
                    'en': 'O Saint Joseph, patron of the dying, assist me at the hour of my death. Intercede that I may breathe my last in the arms of Jesus and Mary, as it was for you. Amen.',
                    'es': 'Oh San José, patrón de los moribundos, asísteme en la hora de mi muerte. Intercede para que pueda expirar entre los brazos de Jesús y María, como te ocurrió a ti. Amén.',
                    'pt': 'Ó São José, patrono dos moribundos, assiste-me na hora da minha morte. Intercede para que eu possa expirar nos braços de Jesus e Maria, como aconteceu contigo. Amém.',
                },
            },
            {
                'intention': {
                    'it': 'Per gli emigranti e i rifugiati',
                    'en': 'For emigrants and refugees',
                    'es': 'Por los emigrantes y refugiados',
                    'pt': 'Pelos emigrantes e refugiados',
                },
                'scripture_ref': 'Mt 2,13-14',
                'prayer': {
                    'it': 'O Giuseppe, che hai vissuto la fuga in Egitto, sii vicino a tutti coloro che sono costretti a lasciare la loro terra. Proteggi chi affronta viaggi pericolosi in cerca di sicurezza. Amen.',
                    'en': 'O Joseph, who lived through the flight into Egypt, be close to all those forced to leave their land. Protect those who face dangerous journeys in search of safety. Amen.',
                    'es': 'Oh José, que viviste la huida a Egipto, permanece cerca de todos los que se ven obligados a abandonar su tierra. Protege a quienes afrontan viajes peligrosos en busca de seguridad. Amén.',
                    'pt': 'Ó José, que viveste a fuga para o Egito, fica perto de todos os que são obrigados a deixar a sua terra. Protege quem enfrenta viagens perigosas em busca de segurança. Amém.',
                },
            },
            {
                'intention': {
                    'it': 'Per la custodia del creato',
                    'en': 'For the care of creation',
                    'es': 'Por el cuidado de la creación',
                    'pt': 'Pelo cuidado da criação',
                },
                'scripture_ref': 'Gn 2,15',
                'prayer': {
                    'it': 'O Giuseppe, lavoratore sapiente che custodiva ciò che ti era affidato, aiutaci a prenderci cura del creato. Che le nostre mani siano mani che coltivano e non distruggono. Amen.',
                    'en': 'O Joseph, wise worker who cared for what was entrusted to you, help us to take care of creation. May our hands be hands that cultivate and do not destroy. Amen.',
                    'es': 'Oh José, sabio trabajador que custodiaba lo que te era encomendado, ayúdanos a cuidar la creación. Que nuestras manos sean manos que cultivan y no destruyen. Amén.',
                    'pt': 'Ó José, trabalhador sábio que cuidava do que lhe era confiado, ajuda-nos a cuidar da criação. Que as nossas mãos sejam mãos que cultivam e não destroem. Amém.',
                },
            },
            {
                'intention': {
                    'it': 'Per affidarsi totalmente a Dio',
                    'en': 'To entrust oneself totally to God',
                    'es': 'Para encomendarse totalmente a Dios',
                    'pt': 'Para se confiar totalmente a Deus',
                },
                'scripture_ref': 'Sal 31,6',
                'prayer': {
                    'it': 'O San Giuseppe, modello di abbandono fiducioso in Dio, insegnami a lasciarmi guidare dalla Provvidenza. Non ho altra sicurezza che la volontà di Dio. In essa mi riposo. Amen.',
                    'en': 'O Saint Joseph, model of trusting abandonment to God, teach me to let myself be guided by Providence. I have no other security than the will of God. In it I rest. Amen.',
                    'es': 'Oh San José, modelo de abandono confiado en Dios, enséñame a dejarme guiar por la Providencia. No tengo otra seguridad que la voluntad de Dios. En ella descanso. Amén.',
                    'pt': 'Ó São José, modelo de abandono confiante em Deus, ensina-me a deixar-me guiar pela Providência. Não tenho outra segurança senão a vontade de Deus. Nela me repouso. Amém.',
                },
            },
        ],
    },

    # -------------------------------------------------------------------------
    'immaculate': {
        'title': {
            'it': "Novena dell'Immacolata Concezione",
            'en': 'Novena of the Immaculate Conception',
            'es': 'Novena de la Inmaculada Concepción',
            'pt': 'Novena da Imaculada Conceição',
        },
        'days': [
            {
                'intention': {'it': 'In lode a Maria Immacolata', 'en': 'In praise of Mary Immaculate', 'es': 'En alabanza a María Inmaculada', 'pt': 'Em louvor a Maria Imaculada'},
                'scripture_ref': 'Lc 1,28',
                'prayer': {
                    'it': 'O Maria, concepita senza peccato originale, prega per noi che ricorriamo a te. Tu sei piena di grazia: ottienici la grazia di cui abbiamo più bisogno. Amen.',
                    'en': 'O Mary, conceived without original sin, pray for us who have recourse to you. You are full of grace: obtain for us the grace we most need. Amen.',
                    'es': 'Oh María, concebida sin pecado original, ruega por nosotros que recurrimos a ti. Estás llena de gracia: obténnos la gracia que más necesitamos. Amén.',
                    'pt': 'Ó Maria, concebida sem pecado original, rogai por nós que recorremos a vós. Estais cheia de graça: obtende para nós a graça de que mais precisamos. Amém.',
                },
            },
            {
                'intention': {'it': 'Per la purezza del cuore', 'en': 'For purity of heart', 'es': 'Por la pureza del corazón', 'pt': 'Pela pureza do coração'},
                'scripture_ref': 'Mt 5,8',
                'prayer': {
                    'it': 'O Maria Immacolata, donaci un cuore puro. Liberaci dai pensieri cattivi, dalle parole offensive, dagli sguardi impuri. Che il tuo candore si rifletta in noi. Amen.',
                    'en': 'O Immaculate Mary, grant us a pure heart. Free us from evil thoughts, offensive words, impure looks. May your purity be reflected in us. Amen.',
                    'es': 'Oh María Inmaculada, concédenos un corazón puro. Líbranos de los pensamientos malos, de las palabras ofensivas, de las miradas impuras. Que tu candor se refleje en nosotros. Amén.',
                    'pt': 'Ó Maria Imaculada, dai-nos um coração puro. Libertai-nos dos pensamentos maus, das palavras ofensivas, dos olhares impuros. Que a vossa pureza se reflita em nós. Amém.',
                },
            },
            {
                'intention': {'it': 'Per la conversione dei peccatori', 'en': 'For the conversion of sinners', 'es': 'Por la conversión de los pecadores', 'pt': 'Pela conversão dos pecadores'},
                'scripture_ref': 'Lc 15,7',
                'prayer': {
                    'it': 'O Maria, rifugio dei peccatori, intercedi per quanti sono lontani da Dio. Tocca i loro cuori con la tua dolcezza e riportali all\'abbraccio misericordioso del Padre. Amen.',
                    'en': 'O Mary, refuge of sinners, intercede for those who are far from God. Touch their hearts with your sweetness and bring them back to the merciful embrace of the Father. Amen.',
                    'es': 'Oh María, refugio de los pecadores, intercede por quienes están lejos de Dios. Toca sus corazones con tu dulzura y devuélvelos al abrazo misericordioso del Padre. Amén.',
                    'pt': 'Ó Maria, refúgio dos pecadores, intercedei pelos que estão longe de Deus. Tocai seus corações com a vossa doçura e trazei-os de volta ao abraço misericordioso do Pai. Amém.',
                },
            },
            {
                'intention': {'it': 'Per i giovani', 'en': 'For the young', 'es': 'Por los jóvenes', 'pt': 'Pelos jovens'},
                'scripture_ref': 'Sal 119,9',
                'prayer': {
                    'it': 'O Maria, giovane tra i giovani, proteggi la gioventù del mondo. Preservala dalle insidie del male e guidala verso il bello, il buono e il vero. Amen.',
                    'en': 'O Mary, young among the young, protect the youth of the world. Preserve them from the snares of evil and guide them toward the beautiful, the good, and the true. Amen.',
                    'es': 'Oh María, joven entre los jóvenes, protege a la juventud del mundo. Presérvala de las asechanzas del mal y guíala hacia lo bello, lo bueno y lo verdadero. Amén.',
                    'pt': 'Ó Maria, jovem entre os jovens, protegei a juventude do mundo. Preservai-a das armadilhas do mal e guiai-a em direção ao belo, ao bom e ao verdadeiro. Amém.',
                },
            },
            {
                'intention': {'it': 'Per la pace nel mondo', 'en': 'For peace in the world', 'es': 'Por la paz en el mundo', 'pt': 'Pela paz no mundo'},
                'scripture_ref': 'Is 2,4',
                'prayer': {
                    'it': 'O Regina della Pace, ottieni al mondo la grazia della pace. Ferma le guerre, ammorbidisci i cuori dei potenti, ispira soluzioni di giustizia. Amen.',
                    'en': 'O Queen of Peace, obtain for the world the grace of peace. Stop wars, soften the hearts of the powerful, inspire solutions of justice. Amen.',
                    'es': 'Oh Reina de la Paz, obtén para el mundo la gracia de la paz. Detén las guerras, ablanda los corazones de los poderosos, inspira soluciones de justicia. Amén.',
                    'pt': 'Ó Rainha da Paz, obtende ao mundo a graça da paz. Estancai as guerras, amolecei os corações dos poderosos, inspirai soluções de justiça. Amém.',
                },
            },
            {
                'intention': {'it': 'Per le mamme', 'en': 'For mothers', 'es': 'Por las madres', 'pt': 'Pelas mães'},
                'scripture_ref': 'Lc 1,42',
                'prayer': {
                    'it': 'O Maria, Madre di Gesù, benedici tutte le mamme del mondo. Donale forza, amore e sapienza. Sostieni quelle che portano un figlio in grembo e quelle che piangono un figlio perduto. Amen.',
                    'en': 'O Mary, Mother of Jesus, bless all the mothers of the world. Grant them strength, love, and wisdom. Support those who carry a child in their womb and those who mourn a lost child. Amen.',
                    'es': 'Oh María, Madre de Jesús, bendice a todas las madres del mundo. Concédeles fuerza, amor y sabiduría. Sostén a las que llevan un hijo en el vientre y a las que lloran un hijo perdido. Amén.',
                    'pt': 'Ó Maria, Mãe de Jesus, abençoai todas as mães do mundo. Dai-lhes força, amor e sabedoria. Sustentai as que carregam um filho no ventre e as que choram um filho perdido. Amém.',
                },
            },
            {
                'intention': {'it': 'Per una fede viva e coraggiosa', 'en': 'For a living and courageous faith', 'es': 'Por una fe viva y valiente', 'pt': 'Por uma fé viva e corajosa'},
                'scripture_ref': 'Lc 1,45',
                'prayer': {
                    'it': 'O Maria, che hai creduto alla Parola di Dio, ravviva la nostra fede. Aiutaci a credere anche quando non vediamo, a sperare anche quando tutto sembra perduto. Amen.',
                    'en': 'O Mary, who believed in the Word of God, rekindle our faith. Help us to believe even when we cannot see, to hope even when everything seems lost. Amen.',
                    'es': 'Oh María, que creíste en la Palabra de Dios, aviva nuestra fe. Ayúdanos a creer incluso cuando no vemos, a esperar incluso cuando todo parece perdido. Amén.',
                    'pt': 'Ó Maria, que crestes na Palavra de Deus, reavivai a nossa fé. Ajudai-nos a crer mesmo quando não vemos, a esperar mesmo quando tudo parece perdido. Amém.',
                },
            },
            {
                'intention': {'it': 'Per i missionari e gli evangelizzatori', 'en': 'For missionaries and evangelizers', 'es': 'Por los misioneros y evangelizadores', 'pt': 'Pelos missionários e evangelizadores'},
                'scripture_ref': 'Mc 16,15',
                'prayer': {
                    'it': 'O Maria, stella dell\'evangelizzazione, proteggi chi porta il Vangelo ai popoli lontani. Sostienili nella fatica, confortali nella solitudine, infiamma il loro amore. Amen.',
                    'en': 'O Mary, star of evangelization, protect those who bring the Gospel to distant peoples. Sustain them in their toil, comfort them in their loneliness, inflame their love. Amen.',
                    'es': 'Oh María, estrella de la evangelización, protege a quienes llevan el Evangelio a los pueblos lejanos. Sostenlos en la fatiga, confórtalos en la soledad, inflama su amor. Amén.',
                    'pt': 'Ó Maria, estrela da evangelização, protegei os que levam o Evangelho aos povos distantes. Sustentai-os no cansaço, confortai-os na solidão, inflamai o seu amor. Amém.',
                },
            },
            {
                'intention': {'it': 'Consacrazione a Maria', 'en': 'Consecration to Mary', 'es': 'Consagración a María', 'pt': 'Consagração a Maria'},
                'scripture_ref': 'Gv 19,27',
                'prayer': {
                    'it': 'O Maria Immacolata, mi consacro a te: il mio cuore, la mia mente, la mia volontà. Portami sempre più vicino a Gesù tuo Figlio. Sii tu a guidare ogni mio passo. Amen.',
                    'en': 'O Immaculate Mary, I consecrate myself to you: my heart, my mind, my will. Lead me ever closer to Jesus your Son. May you guide my every step. Amen.',
                    'es': 'Oh María Inmaculada, me consagro a ti: mi corazón, mi mente, mi voluntad. Llévame siempre más cerca de Jesús, tu Hijo. Sé tú quien guíe cada uno de mis pasos. Amén.',
                    'pt': 'Ó Maria Imaculada, consagro-me a vós: o meu coração, a minha mente, a minha vontade. Conduzi-me sempre mais perto de Jesus, vosso Filho. Sede vós a guiar cada um dos meus passos. Amém.',
                },
            },
        ],
    },

    # -------------------------------------------------------------------------
    'divine_mercy': {
        'title': {
            'it': 'Novena della Divina Misericordia',
            'en': 'Novena of Divine Mercy',
            'es': 'Novena de la Divina Misericordia',
            'pt': 'Novena da Divina Misericórdia',
        },
        'days': [
            {
                'intention': {'it': 'Per tutta l\'umanità, specialmente i peccatori', 'en': 'For all mankind, especially sinners', 'es': 'Por toda la humanidad, especialmente los pecadores', 'pt': 'Por toda a humanidade, especialmente os pecadores'},
                'scripture_ref': 'Gv 3,16',
                'prayer': {
                    'it': 'Gesù, misericordioso, oggi mi inginocchio davanti a te con tutta l\'umanità. Offri al Padre la tua Passione e il tuo Sangue per i peccati del mondo. Misericordia, o Signore! Amen.',
                    'en': 'Merciful Jesus, today I kneel before you with all of humanity. Offer to the Father your Passion and your Blood for the sins of the world. Mercy, O Lord! Amen.',
                    'es': 'Jesús misericordioso, hoy me arrodillo ante ti con toda la humanidad. Ofrece al Padre tu Pasión y tu Sangre por los pecados del mundo. ¡Misericordia, Señor! Amén.',
                    'pt': 'Jesus misericordioso, hoje me ajoelho diante de ti com toda a humanidade. Oferece ao Pai a tua Paixão e o teu Sangue pelos pecados do mundo. Misericórdia, Senhor! Amém.',
                },
            },
            {
                'intention': {'it': 'Per i sacerdoti e i religiosi', 'en': 'For priests and religious', 'es': 'Por los sacerdotes y religiosos', 'pt': 'Pelos sacerdotes e religiosos'},
                'scripture_ref': 'Eb 4,15',
                'prayer': {
                    'it': 'O Gesù, sorgente di misericordia, benedici i tuoi sacerdoti. Santificali nella verità. Che la tua grazia li preservi dal male e li renda autentici mediatori della tua misericordia. Amen.',
                    'en': 'O Jesus, source of mercy, bless your priests. Sanctify them in truth. May your grace preserve them from evil and make them authentic mediators of your mercy. Amen.',
                    'es': 'Oh Jesús, fuente de misericordia, bendice a tus sacerdotes. Santifícalos en la verdad. Que tu gracia los preserve del mal y los haga auténticos mediadores de tu misericordia. Amén.',
                    'pt': 'Ó Jesus, fonte de misericórdia, abençoa os teus sacerdotes. Santifica-os na verdade. Que a tua graça os preserve do mal e os torne autênticos mediadores da tua misericórdia. Amém.',
                },
            },
            {
                'intention': {'it': 'Per le anime pie e fedeli', 'en': 'For devout and faithful souls', 'es': 'Por las almas piadosas y fieles', 'pt': 'Pelas almas piedosas e fiéis'},
                'scripture_ref': 'Ap 14,12',
                'prayer': {
                    'it': 'O Gesù, dona a noi, tuoi fedeli, la perseveranza nella fede. Non permettere che la stanchezza ci vinca. Ravviva il nostro amore, rinforza la nostra speranza. Amen.',
                    'en': 'O Jesus, grant us, your faithful, perseverance in faith. Do not allow weariness to overcome us. Rekindle our love, strengthen our hope. Amen.',
                    'es': 'Oh Jesús, concede a nosotros, tus fieles, la perseverancia en la fe. No permitas que el cansancio nos venza. Reaviva nuestro amor, refuerza nuestra esperanza. Amén.',
                    'pt': 'Ó Jesus, concede a nós, teus fiéis, a perseverança na fé. Não permitas que o cansaço nos vença. Reaviva o nosso amor, reforça a nossa esperança. Amém.',
                },
            },
            {
                'intention': {'it': 'Per i pagani e chi non conosce ancora Gesù', 'en': 'For pagans and those who do not yet know Jesus', 'es': 'Por los paganos y quienes aún no conocen a Jesús', 'pt': 'Pelos pagãos e por quem ainda não conhece Jesus'},
                'scripture_ref': 'At 4,12',
                'prayer': {
                    'it': 'O Gesù, tu sei l\'unico Salvatore. Estendi la tua misericordia a chi non ti conosce ancora. Illumina le loro menti e tocca i loro cuori. Che tutti giungano a conoscerti e amarti. Amen.',
                    'en': 'O Jesus, you are the only Saviour. Extend your mercy to those who do not yet know you. Illuminate their minds and touch their hearts. May all come to know and love you. Amen.',
                    'es': 'Oh Jesús, tú eres el único Salvador. Extiende tu misericordia a quienes aún no te conocen. Ilumina sus mentes y toca sus corazones. Que todos lleguen a conocerte y amarte. Amén.',
                    'pt': 'Ó Jesus, tu és o único Salvador. Estende a tua misericórdia a quem ainda não te conhece. Ilumina as suas mentes e toca os seus corações. Que todos cheguem a conhecer-te e amar-te. Amém.',
                },
            },
            {
                'intention': {'it': 'Per i fratelli separati', 'en': 'For separated brethren', 'es': 'Por los hermanos separados', 'pt': 'Pelos irmãos separados'},
                'scripture_ref': 'Gv 17,21',
                'prayer': {
                    'it': 'O Gesù, che hai pregato perché tutti siano una cosa sola, unisci i cristiani divisi. Sana le ferite storiche, abbatti i muri di incomprensione. Che la tua misericordia ci riunisca. Amen.',
                    'en': 'O Jesus, who prayed that all may be one, unite divided Christians. Heal historical wounds, break down walls of misunderstanding. May your mercy reunite us. Amen.',
                    'es': 'Oh Jesús, que pediste que todos fueran uno, une a los cristianos divididos. Sana las heridas históricas, derriba los muros de incomprensión. Que tu misericordia nos reúna. Amén.',
                    'pt': 'Ó Jesus, que oraste para que todos sejam um, une os cristãos divididos. Cura as feridas históricas, derruba as paredes de incompreensão. Que a tua misericórdia nos reúna. Amém.',
                },
            },
            {
                'intention': {'it': 'Per i miti e umili di cuore', 'en': 'For the meek and humble of heart', 'es': 'Por los mansos y humildes de corazón', 'pt': 'Pelos mansos e humildes de coração'},
                'scripture_ref': 'Mt 11,29',
                'prayer': {
                    'it': 'O Gesù, mite e umile di cuore, fammi simile a te. Liberami dall\'orgoglio e dalla superbia. Che la tua misericordia mi renda capace di servire con gioia. Amen.',
                    'en': 'O Jesus, meek and humble of heart, make me like you. Free me from pride and arrogance. May your mercy make me capable of serving with joy. Amen.',
                    'es': 'Oh Jesús, manso y humilde de corazón, hazme semejante a ti. Líbrame del orgullo y la soberbia. Que tu misericordia me haga capaz de servir con alegría. Amén.',
                    'pt': 'Ó Jesus, manso e humilde de coração, faze-me semelhante a ti. Liberta-me do orgulho e da soberba. Que a tua misericórdia me torne capaz de servir com alegria. Amém.',
                },
            },
            {
                'intention': {'it': 'Per chi si trova nel purgatorio', 'en': 'For souls in purgatory', 'es': 'Por las almas del purgatorio', 'pt': 'Pelas almas do purgatório'},
                'scripture_ref': '2Mac 12,46',
                'prayer': {
                    'it': 'O Gesù, nel tuo Sangue prezioso c\'è la salvezza per tutti. Prega il Padre per le anime del purgatorio: che la tua misericordia acceleri la loro purificazione e le porti presto alla gioia del Paradiso. Amen.',
                    'en': 'O Jesus, in your precious Blood there is salvation for all. Pray to the Father for the souls in purgatory: may your mercy hasten their purification and bring them soon to the joy of Paradise. Amen.',
                    'es': 'Oh Jesús, en tu preciosísima Sangre está la salvación para todos. Ruega al Padre por las almas del purgatorio: que tu misericordia acelere su purificación y las lleve pronto a la alegría del Paraíso. Amén.',
                    'pt': 'Ó Jesus, no teu precioso Sangue está a salvação para todos. Roga ao Pai pelas almas do purgatório: que a tua misericórdia acelere a sua purificação e as leve logo à alegria do Paraíso. Amém.',
                },
            },
            {
                'intention': {'it': 'Per le anime tiepide', 'en': 'For lukewarm souls', 'es': 'Por las almas tibias', 'pt': 'Pelas almas mornas'},
                'scripture_ref': 'Ap 3,16',
                'prayer': {
                    'it': 'O Fuoco di Misericordia, infiamma i cuori tiepidi. Scuotici dall\'indifferenza, liberaci dalla mediocrità spirituale. Che il tuo Amore ci faccia ardere per te. Amen.',
                    'en': 'O Fire of Mercy, inflame lukewarm hearts. Shake us from indifference, free us from spiritual mediocrity. May your Love set us aflame for you. Amen.',
                    'es': 'Oh Fuego de Misericordia, inflama los corazones tibios. Sacúdenos de la indiferencia, líbranos de la mediocridad espiritual. Que tu Amor nos haga arder por ti. Amén.',
                    'pt': 'Ó Fogo de Misericórdia, inflama os corações mornos. Sacuda-nos da indiferença, liberta-nos da mediocridade espiritual. Que o teu Amor nos faça arder por ti. Amém.',
                },
            },
            {
                'intention': {'it': 'Per le anime che hanno perso la speranza', 'en': 'For souls who have lost hope', 'es': 'Por las almas que han perdido la esperanza', 'pt': 'Pelas almas que perderam a esperança'},
                'scripture_ref': 'Lm 3,22-23',
                'prayer': {
                    'it': 'O abisso di Misericordia, nulla è impossibile a te. Togli la disperazione dai cuori smarriti. Restituisci la speranza a chi si è arreso. Tu sei la nostra speranza. Amen.',
                    'en': 'O abyss of Mercy, nothing is impossible for you. Remove despair from lost hearts. Restore hope to those who have given up. You are our hope. Amen.',
                    'es': 'Oh abismo de Misericordia, nada te es imposible. Quita la desesperación de los corazones extraviados. Devuelve la esperanza a quienes se han rendido. Tú eres nuestra esperanza. Amén.',
                    'pt': 'Ó abismo de Misericórdia, nada é impossível para ti. Tira o desespero dos corações perdidos. Restitui a esperança a quem desistiu. Tu és a nossa esperança. Amém.',
                },
            },
        ],
    },

    # -------------------------------------------------------------------------
    'pentecost': {
        'title': {
            'it': 'Novena di Pentecoste',
            'en': 'Pentecost Novena',
            'es': 'Novena de Pentecostés',
            'pt': 'Novena de Pentecostes',
        },
        'days': [
            {
                'intention': {'it': 'Per il dono della Sapienza', 'en': 'For the gift of Wisdom', 'es': 'Por el don de la Sabiduría', 'pt': 'Pelo dom da Sabedoria'},
                'scripture_ref': 'Sap 9,17',
                'prayer': {
                    'it': 'Vieni, Spirito Santo, e donaci la Sapienza. Fa\' che vediamo tutte le cose nella luce di Dio. Che i criteri del mondo cedano ai criteri del Vangelo. Amen.',
                    'en': 'Come, Holy Spirit, and grant us Wisdom. May we see all things in the light of God. May the world\'s criteria yield to the criteria of the Gospel. Amen.',
                    'es': 'Ven, Espíritu Santo, y concédenos la Sabiduría. Haz que veamos todas las cosas a la luz de Dios. Que los criterios del mundo cedan ante los criterios del Evangelio. Amén.',
                    'pt': 'Vem, Espírito Santo, e concede-nos a Sabedoria. Faz que vejamos todas as coisas à luz de Deus. Que os critérios do mundo cedam aos critérios do Evangelho. Amém.',
                },
            },
            {
                'intention': {'it': 'Per il dono dell\'Intelletto', 'en': 'For the gift of Understanding', 'es': 'Por el don del Entendimiento', 'pt': 'Pelo dom do Entendimento'},
                'scripture_ref': 'Sal 119,130',
                'prayer': {
                    'it': 'Vieni, Spirito di Luce, e illumina la nostra mente. Aiutaci a comprendere le Scritture, i misteri della fede, la volontà di Dio. Amen.',
                    'en': 'Come, Spirit of Light, and illuminate our minds. Help us to understand the Scriptures, the mysteries of faith, the will of God. Amen.',
                    'es': 'Ven, Espíritu de Luz, e ilumina nuestra mente. Ayúdanos a comprender las Escrituras, los misterios de la fe, la voluntad de Dios. Amén.',
                    'pt': 'Vem, Espírito de Luz, e ilumina a nossa mente. Ajuda-nos a compreender as Escrituras, os mistérios da fé, a vontade de Deus. Amém.',
                },
            },
            {
                'intention': {'it': 'Per il dono del Consiglio', 'en': 'For the gift of Counsel', 'es': 'Por el don del Consejo', 'pt': 'Pelo dom do Conselho'},
                'scripture_ref': 'Is 11,2',
                'prayer': {
                    'it': 'Vieni, Spirito Consigliere, guidaci nelle scelte difficili della vita. Che ogni nostra decisione sia ispirata dalla tua luce e non dalle passioni. Amen.',
                    'en': 'Come, Spirit of Counsel, guide us in the difficult choices of life. May our every decision be inspired by your light and not by passions. Amen.',
                    'es': 'Ven, Espíritu Consejero, guíanos en las difíciles elecciones de la vida. Que cada una de nuestras decisiones esté inspirada por tu luz y no por las pasiones. Amén.',
                    'pt': 'Vem, Espírito Conselheiro, guia-nos nas escolhas difíceis da vida. Que cada uma das nossas decisões seja inspirada pela tua luz e não pelas paixões. Amém.',
                },
            },
            {
                'intention': {'it': 'Per il dono della Fortezza', 'en': 'For the gift of Fortitude', 'es': 'Por el don de la Fortaleza', 'pt': 'Pelo dom da Fortaleza'},
                'scripture_ref': 'Fil 4,13',
                'prayer': {
                    'it': 'Vieni, Spirito di Fortezza, e rafforza la nostra fede debole. Donaci coraggio per testimoniare il Vangelo anche quando è difficile. Amen.',
                    'en': 'Come, Spirit of Fortitude, and strengthen our weak faith. Grant us courage to witness to the Gospel even when it is difficult. Amen.',
                    'es': 'Ven, Espíritu de Fortaleza, y refuerza nuestra débil fe. Concédenos valor para testimoniar el Evangelio incluso cuando es difícil. Amén.',
                    'pt': 'Vem, Espírito de Fortaleza, e reforça a nossa fé fraca. Concede-nos coragem para testemunhar o Evangelho mesmo quando é difícil. Amém.',
                },
            },
            {
                'intention': {'it': 'Per il dono della Scienza', 'en': 'For the gift of Knowledge', 'es': 'Por el don de la Ciencia', 'pt': 'Pelo dom da Ciência'},
                'scripture_ref': 'Rm 8,28',
                'prayer': {
                    'it': 'Vieni, Spirito di Scienza, e aiutaci a conoscere Dio in tutte le cose create. Che la nostra mente impari a leggere i segni di Dio nella storia e nella natura. Amen.',
                    'en': 'Come, Spirit of Knowledge, and help us to know God in all created things. May our minds learn to read the signs of God in history and in nature. Amen.',
                    'es': 'Ven, Espíritu de Ciencia, y ayúdanos a conocer a Dios en todas las cosas creadas. Que nuestra mente aprenda a leer los signos de Dios en la historia y en la naturaleza. Amén.',
                    'pt': 'Vem, Espírito de Ciência, e ajuda-nos a conhecer Deus em todas as coisas criadas. Que a nossa mente aprenda a ler os sinais de Deus na história e na natureza. Amém.',
                },
            },
            {
                'intention': {'it': 'Per il dono della Pietà', 'en': 'For the gift of Piety', 'es': 'Por el don de la Piedad', 'pt': 'Pelo dom da Piedade'},
                'scripture_ref': 'Gal 4,6',
                'prayer': {
                    'it': 'Vieni, Spirito di Pietà, e fa\' che ci rivolgiamo a Dio come Padre amorevole. Che la preghiera non sia un dovere ma un incontro gioioso con Colui che ci ama. Amen.',
                    'en': 'Come, Spirit of Piety, and help us to turn to God as a loving Father. May prayer not be a duty but a joyful encounter with the One who loves us. Amen.',
                    'es': 'Ven, Espíritu de Piedad, y haz que nos dirijamos a Dios como Padre amoroso. Que la oración no sea un deber sino un encuentro gozoso con Aquel que nos ama. Amén.',
                    'pt': 'Vem, Espírito de Piedade, e faz que nos dirijamos a Deus como Pai amoroso. Que a oração não seja um dever mas um encontro alegre com Aquele que nos ama. Amém.',
                },
            },
            {
                'intention': {'it': 'Per il dono del Timore di Dio', 'en': 'For the gift of Fear of the Lord', 'es': 'Por el don del Temor de Dios', 'pt': 'Pelo dom do Temor de Deus'},
                'scripture_ref': 'Pr 9,10',
                'prayer': {
                    'it': 'Vieni, Spirito Santo, e donaci il santo timore di Dio. Non timore servile, ma timore filiale: quello di chi ama e non vuole offendere chi ama. Amen.',
                    'en': 'Come, Holy Spirit, and grant us holy fear of God. Not servile fear, but filial fear: the fear of one who loves and does not want to offend the one they love. Amen.',
                    'es': 'Ven, Espíritu Santo, y concédenos el santo temor de Dios. No temor servil, sino temor filial: el de quien ama y no quiere ofender a quien ama. Amén.',
                    'pt': 'Vem, Espírito Santo, e concede-nos o santo temor de Deus. Não temor servil, mas temor filial: o de quem ama e não quer ofender quem ama. Amém.',
                },
            },
            {
                'intention': {'it': 'Per i frutti dello Spirito nella nostra vita', 'en': 'For the fruits of the Spirit in our lives', 'es': 'Por los frutos del Espíritu en nuestra vida', 'pt': 'Pelos frutos do Espírito na nossa vida'},
                'scripture_ref': 'Gal 5,22-23',
                'prayer': {
                    'it': 'Spirito Santo, fa\' che nella nostra vita fioriscano i tuoi frutti: amore, gioia, pace, pazienza, benevolenza, bontà, fedeltà, mitezza e dominio di sé. Amen.',
                    'en': 'Holy Spirit, may your fruits flourish in our lives: love, joy, peace, patience, kindness, goodness, faithfulness, gentleness, and self-control. Amen.',
                    'es': 'Espíritu Santo, haz que en nuestra vida florezcan tus frutos: amor, alegría, paz, paciencia, benevolencia, bondad, fidelidad, mansedumbre y dominio propio. Amén.',
                    'pt': 'Espírito Santo, faz que na nossa vida floresçam os teus frutos: amor, alegria, paz, paciência, benevolência, bondade, fidelidade, mansidão e domínio próprio. Amém.',
                },
            },
            {
                'intention': {'it': 'Invocazione a venire nella pienezza', 'en': 'Invocation to come in fullness', 'es': 'Invocación para venir en plenitud', 'pt': 'Invocação para vir em plenitude'},
                'scripture_ref': 'At 2,1-4',
                'prayer': {
                    'it': 'Vieni, Spirito Santo, riempi i cuori dei tuoi fedeli e accendi in essi il fuoco del tuo amore. Manda il tuo Spirito e le cose saranno create, e rinnoverai la faccia della terra. Amen.',
                    'en': 'Come, Holy Spirit, fill the hearts of your faithful and kindle in them the fire of your love. Send forth your Spirit and they shall be created, and you shall renew the face of the earth. Amen.',
                    'es': 'Ven, Espíritu Santo, llena los corazones de tus fieles y enciende en ellos el fuego de tu amor. Envía tu Espíritu y serán creadas las cosas, y renovarás la faz de la tierra. Amén.',
                    'pt': 'Vem, Espírito Santo, enche os corações dos teus fiéis e acende neles o fogo do teu amor. Envia o teu Espírito e as coisas serão criadas, e renovarás a face da terra. Amém.',
                },
            },
        ],
    },
}


def get_novena_rows():
    """Restituisce lista di tuple per INSERT nella tabella novena."""
    rows = []
    for novena_key, novena_data in NOVENE.items():
        for day_idx, day in enumerate(novena_data['days'], start=1):
            for lang in ['it', 'en', 'es', 'pt']:
                title = novena_data['title'][lang]
                intention = day['intention'][lang]
                prayer = day['prayer'][lang]
                scripture_ref = day.get('scripture_ref', '')
                rows.append((novena_key, day_idx, lang, title, intention, prayer, scripture_ref))
    return rows


if __name__ == '__main__':
    rows = get_novena_rows()
    novene_keys = list(NOVENE.keys())
    print(f"Novene: {len(rows)} righe totali")
    print(f"  {len(novene_keys)} novene: {', '.join(novene_keys)}")
    print(f"  {len(novene_keys)} × 9 giorni × 4 lingue = {len(novene_keys)*9*4} attese")
    for key in novene_keys:
        count = sum(1 for r in rows if r[0] == key)
        print(f"  {key}: {count} righe")
