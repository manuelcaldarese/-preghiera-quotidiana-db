#!/usr/bin/env python3
"""
Via Crucis — 14 stazioni × 4 lingue = 56 righe
Testi tradizionali cattolici.
"""

STATIONS = [
    {
        'station': 1,
        'scripture_ref': 'Gv 18,28-19,16',
        'title': {
            'it': 'I stazione: Gesù è condannato a morte',
            'en': '1st Station: Jesus is condemned to death',
            'es': 'I estación: Jesús es condenado a muerte',
            'pt': '1ª estação: Jesus é condenado à morte',
        },
        'meditation': {
            'it': 'Gesù, innocente, viene condannato a morte da Pilato, che cede alla pressione della folla. Egli accetta la sentenza ingiusta con silenzio e umiltà, per amore nostro. Anche noi spesso condanniamo gli innocenti e assolviamo i colpevoli. Chiediamo perdono per le nostre ingiustizie.',
            'en': 'Jesus, innocent, is condemned to death by Pilate, who yields to the pressure of the crowd. He accepts the unjust sentence with silence and humility, for love of us. We too often condemn the innocent and acquit the guilty. Let us ask forgiveness for our injustices.',
            'es': 'Jesús, inocente, es condenado a muerte por Pilato, quien cede a la presión de la multitud. Él acepta la sentencia injusta con silencio y humildad, por amor a nosotros. También nosotros con frecuencia condenamos a los inocentes y absolvemos a los culpables. Pidamos perdón por nuestras injusticias.',
            'pt': 'Jesus, inocente, é condenado à morte por Pilatos, que cede à pressão da multidão. Ele aceita a sentença injusta com silêncio e humildade, por amor a nós. Também nós frequentemente condenamos os inocentes e absolvemos os culpados. Peçamos perdão pelas nossas injustiças.',
        },
        'prayer': {
            'it': 'Ti adoriamo, o Cristo, e ti benediciamo. Perché con la tua santa croce hai redento il mondo.',
            'en': 'We adore you, O Christ, and we bless you. Because by your holy cross you have redeemed the world.',
            'es': 'Te adoramos, oh Cristo, y te bendecimos. Porque con tu santa cruz redimiste al mundo.',
            'pt': 'Nós te adoramos, ó Cristo, e te abençoamos. Porque pela tua santa cruz remiste o mundo.',
        },
    },
    {
        'station': 2,
        'scripture_ref': 'Gv 19,17',
        'title': {
            'it': 'II stazione: Gesù è caricato della croce',
            'en': '2nd Station: Jesus takes up his cross',
            'es': 'II estación: Jesús carga con la cruz',
            'pt': '2ª estação: Jesus carrega a cruz',
        },
        'meditation': {
            'it': 'Gesù riceve la croce sulle spalle. La abbraccia con amore, perché sa che è lo strumento della nostra salvezza. Ogni giorno anche noi riceviamo la nostra croce: la malattia, le difficoltà, le incomprensioni. Impariamo da Gesù ad abbracciarle con fede.',
            'en': 'Jesus receives the cross on his shoulders. He embraces it with love, knowing it is the instrument of our salvation. Each day we too receive our cross: illness, difficulties, misunderstandings. Let us learn from Jesus to embrace them with faith.',
            'es': 'Jesús recibe la cruz sobre sus hombros. La abraza con amor, porque sabe que es el instrumento de nuestra salvación. Cada día también nosotros recibimos nuestra cruz: la enfermedad, las dificultades, los malentendidos. Aprendamos de Jesús a abrazarlas con fe.',
            'pt': 'Jesus recebe a cruz sobre os ombros. Abraça-a com amor, pois sabe que é o instrumento da nossa salvação. A cada dia também nós recebemos a nossa cruz: a doença, as dificuldades, os mal-entendidos. Aprendamos com Jesus a abraçá-las com fé.',
        },
        'prayer': {
            'it': 'Ti adoriamo, o Cristo, e ti benediciamo. Perché con la tua santa croce hai redento il mondo.',
            'en': 'We adore you, O Christ, and we bless you. Because by your holy cross you have redeemed the world.',
            'es': 'Te adoramos, oh Cristo, y te bendecimos. Porque con tu santa cruz redimiste al mundo.',
            'pt': 'Nós te adoramos, ó Cristo, e te abençoamos. Porque pela tua santa cruz remiste o mundo.',
        },
    },
    {
        'station': 3,
        'scripture_ref': 'Is 53,4-6',
        'title': {
            'it': 'III stazione: Gesù cade la prima volta',
            'en': '3rd Station: Jesus falls the first time',
            'es': 'III estación: Jesús cae por primera vez',
            'pt': '3ª estação: Jesus cai pela primeira vez',
        },
        'meditation': {
            'it': 'Schiacciato dal peso della croce e sfinito dalle sofferenze, Gesù cade a terra. Ma si rialza. Le nostre cadute nel peccato non ci devono scoraggiare: come Gesù si è rialzato, anche noi possiamo sempre ricominciare grazie alla sua misericordia.',
            'en': 'Crushed by the weight of the cross and exhausted from suffering, Jesus falls to the ground. But he rises again. Our falls into sin should not discourage us: as Jesus rose again, so too can we always begin again through his mercy.',
            'es': 'Aplastado por el peso de la cruz y agotado por los sufrimientos, Jesús cae a tierra. Pero se levanta. Nuestras caídas en el pecado no deben desanimarnos: así como Jesús se levantó, también nosotros podemos siempre volver a empezar gracias a su misericordia.',
            'pt': 'Esmagado pelo peso da cruz e exausto pelos sofrimentos, Jesus cai por terra. Mas se levanta. As nossas quedas no pecado não devem nos desanimar: como Jesus se levantou, também nós podemos sempre recomeçar graças à sua misericórdia.',
        },
        'prayer': {
            'it': 'Ti adoriamo, o Cristo, e ti benediciamo. Perché con la tua santa croce hai redento il mondo.',
            'en': 'We adore you, O Christ, and we bless you. Because by your holy cross you have redeemed the world.',
            'es': 'Te adoramos, oh Cristo, y te bendecimos. Porque con tu santa cruz redimiste al mundo.',
            'pt': 'Nós te adoramos, ó Cristo, e te abençoamos. Porque pela tua santa cruz remiste o mundo.',
        },
    },
    {
        'station': 4,
        'scripture_ref': 'Lc 2,35',
        'title': {
            'it': 'IV stazione: Gesù incontra sua Madre',
            'en': '4th Station: Jesus meets his Mother',
            'es': 'IV estación: Jesús se encuentra con su Madre',
            'pt': '4ª estação: Jesus encontra sua Mãe',
        },
        'meditation': {
            'it': 'Maria vede suo Figlio portare la croce. Il loro sguardo si incontra: uno sguardo di dolore immenso e di amore infinito. Maria è la Madre che condivide la passione del Figlio. Ella è anche nostra Madre, e ci accompagna nelle nostre sofferenze.',
            'en': 'Mary sees her Son carrying the cross. Their gaze meets: a gaze of immense sorrow and infinite love. Mary is the Mother who shares in her Son\'s passion. She is also our Mother, and accompanies us in our sufferings.',
            'es': 'María ve a su Hijo llevar la cruz. Sus miradas se encuentran: una mirada de inmenso dolor y de amor infinito. María es la Madre que comparte la pasión del Hijo. Ella es también nuestra Madre, y nos acompaña en nuestros sufrimientos.',
            'pt': 'Maria vê seu Filho carregar a cruz. Seus olhares se encontram: um olhar de imenso sofrimento e amor infinito. Maria é a Mãe que partilha a paixão do Filho. Ela é também nossa Mãe, e nos acompanha em nossos sofrimentos.',
        },
        'prayer': {
            'it': 'Ti adoriamo, o Cristo, e ti benediciamo. Perché con la tua santa croce hai redento il mondo.',
            'en': 'We adore you, O Christ, and we bless you. Because by your holy cross you have redeemed the world.',
            'es': 'Te adoramos, oh Cristo, y te bendecimos. Porque con tu santa cruz redimiste al mundo.',
            'pt': 'Nós te adoramos, ó Cristo, e te abençoamos. Porque pela tua santa cruz remiste o mundo.',
        },
    },
    {
        'station': 5,
        'scripture_ref': 'Mc 15,21',
        'title': {
            'it': 'V stazione: Simone di Cirene aiuta Gesù a portare la croce',
            'en': '5th Station: Simon of Cyrene helps Jesus carry the cross',
            'es': 'V estación: Simón de Cirene ayuda a Jesús a llevar la cruz',
            'pt': '5ª estação: Simão de Cirene ajuda Jesus a carregar a cruz',
        },
        'meditation': {
            'it': 'I soldati costringono Simone di Cirene a portare la croce con Gesù. Simone forse era restio, ma poi accettò. In ogni persona che soffre, è Gesù che ci chiede aiuto. Quando alleviamo il peso degli altri, alleviamo il peso di Gesù.',
            'en': 'The soldiers force Simon of Cyrene to carry the cross with Jesus. Simon may have been reluctant, but then accepted. In every person who suffers, it is Jesus who asks for our help. When we lighten the burden of others, we lighten the burden of Jesus.',
            'es': 'Los soldados obligan a Simón de Cirene a llevar la cruz con Jesús. Simón quizás era reacio, pero luego aceptó. En cada persona que sufre, es Jesús quien nos pide ayuda. Cuando aliviamos el peso de los demás, aliviamos el peso de Jesús.',
            'pt': 'Os soldados obrigam Simão de Cirene a carregar a cruz com Jesus. Simão talvez estivesse relutante, mas depois aceitou. Em cada pessoa que sofre, é Jesus que nos pede ajuda. Quando aliviamos o fardo dos outros, aliviamos o fardo de Jesus.',
        },
        'prayer': {
            'it': 'Ti adoriamo, o Cristo, e ti benediciamo. Perché con la tua santa croce hai redento il mondo.',
            'en': 'We adore you, O Christ, and we bless you. Because by your holy cross you have redeemed the world.',
            'es': 'Te adoramos, oh Cristo, y te bendecimos. Porque con tu santa cruz redimiste al mundo.',
            'pt': 'Nós te adoramos, ó Cristo, e te abençoamos. Porque pela tua santa cruz remiste o mundo.',
        },
    },
    {
        'station': 6,
        'scripture_ref': 'Is 53,3',
        'title': {
            'it': 'VI stazione: La Veronica asciuga il volto di Gesù',
            'en': '6th Station: Veronica wipes the face of Jesus',
            'es': 'VI estación: La Verónica enjuga el rostro de Jesús',
            'pt': '6ª estação: Verônica enxuga o rosto de Jesus',
        },
        'meditation': {
            'it': 'Una donna coraggiosa, chiamata Veronica, si fa avanti tra la folla e asciuga il volto di Gesù coperto di sudore e sangue. Come segno di gratitudine, il volto di Gesù rimane impresso sul panno. Un piccolo gesto di amore lascia un segno eterno.',
            'en': 'A courageous woman, called Veronica, steps forward through the crowd and wipes the face of Jesus, covered in sweat and blood. As a sign of gratitude, the face of Jesus remains imprinted on the cloth. A small act of love leaves an eternal mark.',
            'es': 'Una mujer valiente, llamada Verónica, se adelanta entre la multitud y enjuga el rostro de Jesús cubierto de sudor y sangre. Como señal de gratitud, el rostro de Jesús queda impreso en el paño. Un pequeño gesto de amor deja una marca eterna.',
            'pt': 'Uma mulher corajosa, chamada Verônica, avança pela multidão e enxuga o rosto de Jesus coberto de suor e sangue. Como sinal de gratidão, o rosto de Jesus fica impresso no pano. Um pequeno gesto de amor deixa uma marca eterna.',
        },
        'prayer': {
            'it': 'Ti adoriamo, o Cristo, e ti benediciamo. Perché con la tua santa croce hai redento il mondo.',
            'en': 'We adore you, O Christ, and we bless you. Because by your holy cross you have redeemed the world.',
            'es': 'Te adoramos, oh Cristo, y te bendecimos. Porque con tu santa cruz redimiste al mundo.',
            'pt': 'Nós te adoramos, ó Cristo, e te abençoamos. Porque pela tua santa cruz remiste o mundo.',
        },
    },
    {
        'station': 7,
        'scripture_ref': 'Is 53,6',
        'title': {
            'it': 'VII stazione: Gesù cade la seconda volta',
            'en': '7th Station: Jesus falls the second time',
            'es': 'VII estación: Jesús cae por segunda vez',
            'pt': '7ª estação: Jesus cai pela segunda vez',
        },
        'meditation': {
            'it': 'Gesù cade di nuovo. Le forze vengono meno. Eppure si rialza ancora, mosso dall\'amore per noi. Quando ricadiamo nelle stesse debolezze e nei medesimi peccati, non perdiamo la speranza. Gesù ci conosce e ci ama nella nostra fragilità.',
            'en': 'Jesus falls again. His strength fails. Yet he rises again, moved by love for us. When we fall back into the same weaknesses and the same sins, let us not lose hope. Jesus knows us and loves us in our fragility.',
            'es': 'Jesús cae de nuevo. Las fuerzas le fallan. Sin embargo se levanta otra vez, movido por el amor hacia nosotros. Cuando recaemos en las mismas debilidades y en los mismos pecados, no perdamos la esperanza. Jesús nos conoce y nos ama en nuestra fragilidad.',
            'pt': 'Jesus cai novamente. As forças o abandonam. Mesmo assim ele se levanta de novo, movido pelo amor a nós. Quando recaímos nas mesmas fraquezas e nos mesmos pecados, não percamos a esperança. Jesus nos conhece e nos ama em nossa fragilidade.',
        },
        'prayer': {
            'it': 'Ti adoriamo, o Cristo, e ti benediciamo. Perché con la tua santa croce hai redento il mondo.',
            'en': 'We adore you, O Christ, and we bless you. Because by your holy cross you have redeemed the world.',
            'es': 'Te adoramos, oh Cristo, y te bendecimos. Porque con tu santa cruz redimiste al mundo.',
            'pt': 'Nós te adoramos, ó Cristo, e te abençoamos. Porque pela tua santa cruz remiste o mundo.',
        },
    },
    {
        'station': 8,
        'scripture_ref': 'Lc 23,27-31',
        'title': {
            'it': 'VIII stazione: Gesù consola le donne di Gerusalemme',
            'en': '8th Station: Jesus consoles the women of Jerusalem',
            'es': 'VIII estación: Jesús consuela a las mujeres de Jerusalén',
            'pt': '8ª estação: Jesus consola as mulheres de Jerusalém',
        },
        'meditation': {
            'it': 'Alcune donne piangono per Gesù lungo la strada. Egli, nonostante la sua sofferenza, si ferma e le consola: "Non piangete su di me, ma piangete su voi stesse e sui vostri figli." Gesù, anche nel suo dolore, pensa agli altri. Impariamo a uscire da noi stessi per preoccuparci degli altri.',
            'en': 'Some women weep for Jesus along the road. He, despite his suffering, stops and consoles them: "Do not weep for me, but weep for yourselves and for your children." Jesus, even in his pain, thinks of others. Let us learn to step outside ourselves to care for others.',
            'es': 'Algunas mujeres lloran por Jesús a lo largo del camino. Él, a pesar de su sufrimiento, se detiene y las consuela: "No lloréis por mí, sino llorad por vosotras mismas y por vuestros hijos." Jesús, incluso en su dolor, piensa en los demás. Aprendamos a salir de nosotros mismos para preocuparnos por los demás.',
            'pt': 'Algumas mulheres choram por Jesus ao longo do caminho. Ele, apesar do seu sofrimento, para e as consola: "Não choreis por mim, mas chorai por vós mesmas e pelos vossos filhos." Jesus, mesmo na sua dor, pensa nos outros. Aprendamos a sair de nós mesmos para nos preocuparmos com os outros.',
        },
        'prayer': {
            'it': 'Ti adoriamo, o Cristo, e ti benediciamo. Perché con la tua santa croce hai redento il mondo.',
            'en': 'We adore you, O Christ, and we bless you. Because by your holy cross you have redeemed the world.',
            'es': 'Te adoramos, oh Cristo, y te bendecimos. Porque con tu santa cruz redimiste al mundo.',
            'pt': 'Nós te adoramos, ó Cristo, e te abençoamos. Porque pela tua santa cruz remiste o mundo.',
        },
    },
    {
        'station': 9,
        'scripture_ref': 'Lc 22,44',
        'title': {
            'it': 'IX stazione: Gesù cade la terza volta',
            'en': '9th Station: Jesus falls the third time',
            'es': 'IX estación: Jesús cae por tercera vez',
            'pt': '9ª estação: Jesus cai pela terceira vez',
        },
        'meditation': {
            'it': 'Gesù cade per la terza volta, ormai vicino al Calvario. È esausto, umiliato, coperto di sangue. Ma il suo amore è più forte di tutto. Quando siamo a terra e non riusciamo più ad alzarci, ricordiamo che Gesù conosce quella sensazione e ci tende la mano.',
            'en': 'Jesus falls a third time, now close to Calvary. He is exhausted, humiliated, covered in blood. But his love is stronger than everything. When we are on the ground and can no longer rise, let us remember that Jesus knows that feeling and reaches out his hand to us.',
            'es': 'Jesús cae por tercera vez, ya cerca del Calvario. Está agotado, humillado, cubierto de sangre. Pero su amor es más fuerte que todo. Cuando estamos en el suelo y ya no podemos levantarnos, recordemos que Jesús conoce esa sensación y nos tiende la mano.',
            'pt': 'Jesus cai pela terceira vez, já perto do Calvário. Está exausto, humilhado, coberto de sangue. Mas o seu amor é mais forte que tudo. Quando estamos no chão e não conseguimos mais nos levantar, lembremos que Jesus conhece essa sensação e nos estende a mão.',
        },
        'prayer': {
            'it': 'Ti adoriamo, o Cristo, e ti benediciamo. Perché con la tua santa croce hai redento il mondo.',
            'en': 'We adore you, O Christ, and we bless you. Because by your holy cross you have redeemed the world.',
            'es': 'Te adoramos, oh Cristo, y te bendecimos. Porque con tu santa cruz redimiste al mundo.',
            'pt': 'Nós te adoramos, ó Cristo, e te abençoamos. Porque pela tua santa cruz remiste o mundo.',
        },
    },
    {
        'station': 10,
        'scripture_ref': 'Gv 19,23-24',
        'title': {
            'it': 'X stazione: Gesù è spogliato delle vesti',
            'en': '10th Station: Jesus is stripped of his garments',
            'es': 'X estación: Jesús es despojado de sus vestidos',
            'pt': '10ª estação: Jesus é despojado de suas vestes',
        },
        'meditation': {
            'it': 'Sul Calvario, i soldati tolgono le vesti a Gesù, rinnovando le sue piaghe. Egli viene spogliato di tutto, anche della sua dignità. Gesù ha accettato questa umiliazione per rivestirci della grazia di Dio. Chiediamogli di spogliarci dai nostri attaccamenti per rivestirci di lui.',
            'en': 'On Calvary, the soldiers strip Jesus of his garments, reopening his wounds. He is stripped of everything, even his dignity. Jesus accepted this humiliation to clothe us in the grace of God. Let us ask him to strip us of our attachments so that we may be clothed in him.',
            'es': 'En el Calvario, los soldados despojan a Jesús de sus vestidos, renovando sus llagas. Es despojado de todo, incluso de su dignidad. Jesús aceptó esta humillación para revestirnos de la gracia de Dios. Pidámosle que nos despoje de nuestros apegos para revestirnos de Él.',
            'pt': 'No Calvário, os soldados despem Jesus de suas vestes, renovando suas chagas. Ele é despojado de tudo, até da sua dignidade. Jesus aceitou esta humilhação para nos revestir da graça de Deus. Peçamos-lhe que nos despoje de nossos apegos para nos revestirmos dEle.',
        },
        'prayer': {
            'it': 'Ti adoriamo, o Cristo, e ti benediciamo. Perché con la tua santa croce hai redento il mondo.',
            'en': 'We adore you, O Christ, and we bless you. Because by your holy cross you have redeemed the world.',
            'es': 'Te adoramos, oh Cristo, y te bendecimos. Porque con tu santa cruz redimiste al mundo.',
            'pt': 'Nós te adoramos, ó Cristo, e te abençoamos. Porque pela tua santa cruz remiste o mundo.',
        },
    },
    {
        'station': 11,
        'scripture_ref': 'Gv 19,18',
        'title': {
            'it': 'XI stazione: Gesù è inchiodato alla croce',
            'en': '11th Station: Jesus is nailed to the cross',
            'es': 'XI estación: Jesús es clavado en la cruz',
            'pt': '11ª estação: Jesus é pregado na cruz',
        },
        'meditation': {
            'it': 'Gesù viene disteso sulla croce e inchiodato. I chiodi trapassano le mani e i piedi che hanno fatto tanto bene. Quelle mani che hanno guarito i malati, accarezzato i bambini, benedetto i poveri, ora sono immobilizzate per amore nostro. "Padre, perdona loro perché non sanno quello che fanno."',
            'en': 'Jesus is laid on the cross and nailed to it. The nails pierce the hands and feet that have done so much good. Those hands that healed the sick, caressed children, blessed the poor, are now immobilized for love of us. "Father, forgive them, for they know not what they do."',
            'es': 'Jesús es tendido sobre la cruz y clavado en ella. Los clavos traspasan las manos y los pies que tanto bien han hecho. Esas manos que han curado a los enfermos, acariciado a los niños, bendecido a los pobres, ahora están inmovilizadas por amor a nosotros. "Padre, perdónalos, porque no saben lo que hacen."',
            'pt': 'Jesus é deitado sobre a cruz e pregado nela. Os pregos atravessam as mãos e os pés que tanto bem fizeram. Aquelas mãos que curaram os doentes, acariciaram as crianças, abençoaram os pobres, agora estão imobilizadas por amor a nós. "Pai, perdoa-lhes, porque não sabem o que fazem."',
        },
        'prayer': {
            'it': 'Ti adoriamo, o Cristo, e ti benediciamo. Perché con la tua santa croce hai redento il mondo.',
            'en': 'We adore you, O Christ, and we bless you. Because by your holy cross you have redeemed the world.',
            'es': 'Te adoramos, oh Cristo, y te bendecimos. Porque con tu santa cruz redimiste al mundo.',
            'pt': 'Nós te adoramos, ó Cristo, e te abençoamos. Porque pela tua santa cruz remiste o mundo.',
        },
    },
    {
        'station': 12,
        'scripture_ref': 'Gv 19,25-30',
        'title': {
            'it': 'XII stazione: Gesù muore in croce',
            'en': '12th Station: Jesus dies on the cross',
            'es': 'XII estación: Jesús muere en la cruz',
            'pt': '12ª estação: Jesus morre na cruz',
        },
        'meditation': {
            'it': 'Dopo tre ore di agonia, Gesù grida: "Tutto è compiuto!" e china il capo, spirando. La morte di Dio fatto uomo: il più grande atto d\'amore della storia. Non c\'è peccato così grande da non poter essere perdonato dal sangue di Cristo. Inginocchiamoci in adorazione.',
            'en': 'After three hours of agony, Jesus cries out: "It is finished!" and bows his head, breathing his last. The death of God made man: the greatest act of love in history. There is no sin so great that it cannot be forgiven by the blood of Christ. Let us kneel in adoration.',
            'es': 'Después de tres horas de agonía, Jesús clama: "¡Todo está cumplido!" e inclina la cabeza, expirando. La muerte de Dios hecho hombre: el mayor acto de amor de la historia. No hay pecado tan grande que no pueda ser perdonado por la sangre de Cristo. Arrodillémonos en adoración.',
            'pt': 'Após três horas de agonia, Jesus clama: "Tudo está consumado!" e inclina a cabeça, expirando. A morte de Deus feito homem: o maior ato de amor da história. Não há pecado tão grande que não possa ser perdoado pelo sangue de Cristo. Ajoelhemo-nos em adoração.',
        },
        'prayer': {
            'it': 'Ti adoriamo, o Cristo, e ti benediciamo. Perché con la tua santa croce hai redento il mondo.',
            'en': 'We adore you, O Christ, and we bless you. Because by your holy cross you have redeemed the world.',
            'es': 'Te adoramos, oh Cristo, y te bendecimos. Porque con tu santa cruz redimiste al mundo.',
            'pt': 'Nós te adoramos, ó Cristo, e te abençoamos. Porque pela tua santa cruz remiste o mundo.',
        },
    },
    {
        'station': 13,
        'scripture_ref': 'Gv 19,38-40',
        'title': {
            'it': 'XIII stazione: Gesù è deposto dalla croce',
            'en': '13th Station: Jesus is taken down from the cross',
            'es': 'XIII estación: Jesús es bajado de la cruz',
            'pt': '13ª estação: Jesus é tirado da cruz',
        },
        'meditation': {
            'it': 'Il corpo di Gesù viene deposto dalla croce e consegnato nelle braccia di Maria. La Pietà: la Madre stringe al petto il Figlio morto. Quale dolore immenso! Maria ha accettato questo dolore per amore nostro. Affidiamoci a lei, che conosce il dolore e sa consolare.',
            'en': 'The body of Jesus is taken down from the cross and placed in Mary\'s arms. The Pietà: the Mother holds her dead Son to her breast. What immense grief! Mary accepted this sorrow for love of us. Let us entrust ourselves to her, who knows sorrow and knows how to console.',
            'es': 'El cuerpo de Jesús es bajado de la cruz y colocado en los brazos de María. La Pietà: la Madre estrecha contra su pecho al Hijo muerto. ¡Qué dolor inmenso! María aceptó este dolor por amor a nosotros. Encomendémonos a ella, que conoce el dolor y sabe consolar.',
            'pt': 'O corpo de Jesus é tirado da cruz e entregue nos braços de Maria. A Pietà: a Mãe estreita ao peito o Filho morto. Que dor imensa! Maria aceitou esta dor por amor a nós. Confiemos a ela, que conhece a dor e sabe consolar.',
        },
        'prayer': {
            'it': 'Ti adoriamo, o Cristo, e ti benediciamo. Perché con la tua santa croce hai redento il mondo.',
            'en': 'We adore you, O Christ, and we bless you. Because by your holy cross you have redeemed the world.',
            'es': 'Te adoramos, oh Cristo, y te bendecimos. Porque con tu santa cruz redimiste al mundo.',
            'pt': 'Nós te adoramos, ó Cristo, e te abençoamos. Porque pela tua santa cruz remiste o mundo.',
        },
    },
    {
        'station': 14,
        'scripture_ref': 'Gv 19,41-42',
        'title': {
            'it': 'XIV stazione: Gesù è sepolto nel sepolcro',
            'en': '14th Station: Jesus is laid in the tomb',
            'es': 'XIV estación: Jesús es sepultado en el sepulcro',
            'pt': '14ª estação: Jesus é sepultado no sepulcro',
        },
        'meditation': {
            'it': 'Il corpo di Gesù viene avvolto in bende e deposto in un sepolcro nuovo, nel giardino. La pietra viene chiusa. Sembra la fine. Ma è l\'inizio: il sabato del silenzio precede la Resurrezione. Nelle nostre notti oscure, fidiamoci: Dio trasforma ogni tomba in grembo di vita nuova.',
            'en': 'The body of Jesus is wrapped in linen cloths and laid in a new tomb, in the garden. The stone is sealed. It seems like the end. But it is the beginning: the Saturday of silence precedes the Resurrection. In our dark nights, let us trust: God transforms every tomb into a womb of new life.',
            'es': 'El cuerpo de Jesús es envuelto en vendas y depositado en un sepulcro nuevo, en el jardín. La piedra es sellada. Parece el fin. Pero es el comienzo: el sábado del silencio precede a la Resurrección. En nuestras noches oscuras, confiemos: Dios transforma cada tumba en seno de vida nueva.',
            'pt': 'O corpo de Jesus é envolto em panos e depositado num sepulcro novo, no jardim. A pedra é fechada. Parece o fim. Mas é o começo: o sábado do silêncio precede a Ressurreição. Em nossas noites escuras, confiemos: Deus transforma todo sepulcro em ventre de vida nova.',
        },
        'prayer': {
            'it': 'Ti adoriamo, o Cristo, e ti benediciamo. Perché con la tua santa croce hai redento il mondo.',
            'en': 'We adore you, O Christ, and we bless you. Because by your holy cross you have redeemed the world.',
            'es': 'Te adoramos, oh Cristo, y te bendecimos. Porque con tu santa cruz redimiste al mundo.',
            'pt': 'Nós te adoramos, ó Cristo, e te abençoamos. Porque pela tua santa cruz remiste o mundo.',
        },
    },
]


def get_via_crucis_rows():
    """Restituisce lista di tuple per INSERT nella tabella via_crucis."""
    rows = []
    for s in STATIONS:
        for lang in ['it', 'en', 'es', 'pt']:
            rows.append((
                s['station'],
                lang,
                s['title'][lang],
                s['meditation'][lang],
                s['prayer'][lang],
                s['scripture_ref'],
            ))
    return rows


if __name__ == '__main__':
    rows = get_via_crucis_rows()
    print(f"Via Crucis: {len(rows)} righe ({len(STATIONS)} stazioni × 4 lingue)")
    for r in rows[:4]:
        print(f"  Stazione {r[0]} [{r[1]}]: {r[2][:60]}...")
