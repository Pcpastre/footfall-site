BODY = {}

BODY["comecar"] = """
<p>Footfall se juega caminando de verdad. El mapa es tu ciudad por GPS, y solo avanzas cuando caminas. Esta guía te lleva desde el primer toque hasta tu primera sesión en la calle.</p>

<h2>Cuenta</h2>
<p>El juego necesita una cuenta con correo y contraseña: es la que guarda tu personaje, la base y el progreso en la nube. En la pantalla de inicio, toca <kbd>ENTRAR / CREAR CUENTA</kbd>. La contraseña tiene al menos 8 caracteres y el registro se confirma con un código de 6 dígitos que llega por correo.</p>

<h2>Tu sobreviviente</h2>
<ol class="steps">
<li><b>Antes de salir a caminar:</b> lee los avisos de seguridad y toca <kbd>ENTENDIDO, VAMOS</kbd>.</li>
<li><b>Apariencia:</b> rostro, cabello, piel y ropa.</li>
<li><b>Profesión y rasgos:</b> cada profesión da habilidades y un saldo de puntos. Los rasgos positivos gastan puntos; los negativos los devuelven.</li>
</ol>
<p>Algunas profesiones para empezar:</p>
<ul>
<li><b>Desempleado(a):</b> ningún bono, pero el mayor saldo de puntos para rasgos.</li>
<li><b>Policía</b> y <b>Militar veterano(a):</b> mejores con armas de fuego (el militar ya viene insensible al pánico).</li>
<li><b>Enfermero(a)</b> y <b>Médico(a):</b> tratan heridas más rápido y con menos fallas.</li>
<li><b>Carpintero(a):</b> construye y repara la base mejor.</li>
<li><b>Repartidor(a):</b> empieza con el barrio ya descubierto en el mapa, y la distancia caminada rinde más.</li>
<li><b>Ladrón(a):</b> registra 1,5× más rápido y hace menos ruido.</li>
</ul>
<p>Rasgos útiles: <b>Pasos ligeros</b> (menos ruido), <b>Ojos de águila</b> (ve más lejos), <b>Organizado</b> (mochila más grande), <b>Piel gruesa</b> (los golpes se vuelven menos heridas). Cuidado con <b>Hogareño</b> (se cansa lejos de la base) y <b>Fumador</b> (necesita cigarrillos).</p>
<p>Empiezas con el kit básico en la mochila: bate, revólver con balas, vendajes, agua, comida, vaqueros y mochila escolar.</p>
<div class="tip warn"><b>La muerte es permanente</b>Si el personaje muere, él y sus habilidades se van. La base, los cofres y el depósito de la radio quedan para el siguiente.</div>

<h2>La primera noche</h2>
<p>Antes del mapa, el juego ofrece <b>La última entrega</b>: eres un cartero en una noche de tormenta, y ella te enseña a caminar agachado, registrar, golpear, empujar y disparar. Puedes saltarla con <kbd>IR DIRECTO A LA CIUDAD</kbd> y jugarla después desde la estante de memorias.</p>

<h2>Sesión</h2>
<p>En el mapa, toca <kbd>INICIAR SESIÓN</kbd> en la barra de abajo. Desde ahí tu personaje camina contigo. Para parar, abre el menú <kbd>⋯</kbd>:</p>
<ul>
<li><kbd>Dormir (terminar aquí)</kbd> en la base, en un puesto avanzado o en una tienda de campaña: el personaje descansa y recupera cansancio y vida.</li>
<li><kbd>Terminar sesión</kbd> en cualquier otro lugar: no pierdes nada, pero el descanso es malo.</li>
</ul>

<h2>Ver y ser visto</h2>
<ul>
<li>Ves en un cono de 110° frente a ti, hasta 120 m de día y 40 m de noche. Los edificios tapan la vista.</li>
<li>El cono sigue la parte de arriba del celular (brújula). Si la brújula estorba, apágala en Ajustes y usa el stick para mirar.</li>
<li>Los zombis te ven a unos 15 m de día y 8 m de noche, pero con la linterna encendida te ven a 30 m.</li>
<li>Caminar hace poco ruido; correr hace mucho más. El ruido atrae a los que están cerca.</li>
</ul>

<h2>Cuanto más caminas, mejor el botín</h2>
<p>La distancia caminada en la sesión aumenta la probabilidad de encontrar objetos raros (hasta 15%). Solo cuenta caminando a pie: por encima de unos 25 km/h durante algunos segundos el juego entiende que vas en un vehículo, la distancia deja de contar y el ruido llega al máximo.</p>

<div class="tip"><b>Al cruzar la calle</b>En las avenidas, los zombis se detienen y no empieza ninguna pelea: aparece "Cruza con cuidado". Mira la calle de verdad, no la pantalla. Nunca juegues mientras manejas.</div>
"""

BODY["saque"] = """
<p>Los mercados, farmacias, comisarías, gasolineras, escuelas, tiendas y casas de tu barrio están en el juego. Cada tipo de lugar tiene sus hallazgos y sus peligros.</p>

<h2>Por la puerta o entrando</h2>
<p>A menos de 35 m de un lugar (casas: pegado a ellas), toca <kbd>Saquear</kbd>. Eliges:</p>
<ul>
<li><b>Por la puerta:</b> rápido, solo los muebles de la entrada y sin objetos raros.</li>
<li><b>Entrar:</b> abre la pantalla de acción dentro del edificio. Más muebles, más probabilidad de algo raro y más zombis. Los edificios pueden tener pisos (<kbd>SUBIR</kbd> / <kbd>BAJAR</kbd>).</li>
</ul>
<p>Si te alejas más de 20 m en medio del saqueo, se interrumpe.</p>

<h2>Muebles y ruido</h2>
<p>Cada mueble tiene un tiempo para registrarlo y un nivel de ruido: <b>silencioso</b>, <b>ruido moderado</b> o <b>ruido fuerte</b>. Un cajón tarda 1 s; una caja registradora, 2,5 s y hace ruido; un arsenal cerrado, 5 s y mucho ruido. Quédate quieto mientras registras y toca <kbd>Tomar todo</kbd> al final.</p>
<ul>
<li>A veces el mueble está vacío.</li>
<li>Registrar vidrio y latas puede cortarte la mano (esquirla).</li>
<li>Las puertas cerradas se abren con palanca (3 s, con ruido) o cuando un zombi de adentro rompe la puerta.</li>
</ul>

<h2>Reabastecimiento cada semana</h2>
<p>Un lugar saqueado queda marcado como "ya saqueado" durante 7 días; después se llena de nuevo. Las existencias son las mismas para todos: si aparece "Otro sobreviviente lo tomó antes", alguien llegó primero.</p>

<h2>Cuerpos</h2>
<p>Los zombis abatidos quedan en el suelo durante 2 horas. Cada pelea deja una pila de cuerpos: <kbd>Registrar todos</kbd> los revisa todos de una vez. Los cuerpos traen cosas de los bolsillos, trapos y, a veces, sellos. Los zombis de uniforme (policía, bombero, médico…) llevan lo que usaban en vida, y a veces el uniforme entero.</p>

<h2>Mochila y peso</h2>
<p>Lo que puedes cargar es la suma de los bolsillos de la ropa y de la mochila:</p>
<ul>
<li>Bolsillos del cuerpo: 4 kg, más los bolsillos de pantalones, chalecos, riñonera y bolsa de muslo.</li>
<li>Mochilas: escolar 6 kg, de gimnasio 5, de senderismo 10, táctica 12, de expedición 16.</li>
<li>Fuerza, Organizado y Desorganizado cambian ese límite.</li>
</ul>
<p>Por encima del límite aparece <b>Carga pesada</b>: eres más lento en la pelea y más ruidoso en el mapa.</p>
<p>El cinturón tiene 2 espacios para lo que necesitas a mano rápido (el 3.º con chaleco táctico o mochila táctica). Las armas largas van en la espalda.</p>
<div class="tip"><b>Consejo</b>Los medicamentos, la munición, las cosas para lanzar y las pilas van primero a los bolsillos. En la pelea, sacar cualquier otra cosa del fondo de la mochila tarda 2,5 s.</div>

<h2>Búnkeres militares</h2>
<p>Cada mes, algunas plazas se vuelven búnkeres con 3 a 6 pisos hacia abajo, cada vez más oscuros y más peligrosos, y con un botín cada vez mejor. Cada piso empieza en una sala segura, donde los zombis no entran. El generador de un piso enciende la luz con 1 biodiésel. La puerta del cofre del fondo se abre con la tarjeta de acceso, o con palanca en 60 s y mucho ruido. El búnker se reabastece al mes siguiente.</p>
"""

BODY["combate"] = """
<p>Cuando un zombi que te persigue llega a 25 m, el juego te pide que te detengas en un lugar seguro y abre la <b>pantalla de acción</b>: la escena en pixel art del lugar donde estás, con las calles, los autos y los edificios de verdad. También puedes abrirla con el botón grande <kbd>Pantalla de acción</kbd> del mapa.</p>
<p>Los zombis a menos de 120 m entran en la pelea, unos pocos a la vez. En la base a salvo o cruzando una avenida, no empieza ninguna pelea.</p>

<h2>Los tres controles</h2>
<p>Elige en Ajustes → <kbd>CONTROLES</kbd> (o tocando la tarjeta de estado durante la pelea):</p>
<ul>
<li><b>Simple</b> (predeterminado): un stick para caminar y el botón <kbd>PELEAR</kbd>. Con él activado, encaras al zombi más cercano; toca la mitad derecha de la pantalla para golpear o disparar y la izquierda para empujar. Correr lo desactiva.</li>
<li><b>Dos sticks:</b> el derecho apunta; tocar la pantalla golpea y empuja.</li>
<li><b>Automático:</b> solo el stick de caminar; el golpe, el disparo y el empujón salen solos.</li>
</ul>

<h2>Empujar</h2>
<p>El empujón es tu mejor defensa: derriba o desequilibra, te suelta de quien te agarró y baja el pánico. Gasta aliento y tiene una pequeña espera entre uno y otro.</p>

<h2>Apuntar y acertar</h2>
<ul>
<li>Elige el <kbd>OBJETIVO</kbd>: cabeza, cuerpo o piernas.</li>
<li>En la cabeza, el golpe hace más daño, pero puede resbalar al hombro (menos con más habilidad). El disparo en la cabeza hace 2,5× de daño.</li>
<li>Las piernas destruidas hacen que el zombi se arrastre.</li>
<li>Los aciertos con la punta del arma pueden ser críticos.</li>
</ul>

<h2>Aliento</h2>
<p>Correr gasta aliento rápido; quieto, vuelve. Con poco aliento, los golpes pierden fuerza. El cansancio, la fiebre, el frío, el calor y el dolor reducen el aliento máximo.</p>

<h2>Agacharse</h2>
<p><kbd>AGACHARSE</kbd> te vuelve lento y no puedes correr, pero los zombis distraídos tardan el doble en notarte y tienen que estar mucho más cerca. Por detrás, fuera de su vista, puedes abatirlos en silencio.</p>

<h2>Armas</h2>
<ul>
<li><b>Blancas</b> (cuchillo, bate, machete, hacha, mazo, katana…): se desgastan con cada golpe que acierta y se rompen. Se pueden reparar en el banco de trabajo o con cinta y clavos.</li>
<li><b>De fuego</b> (pistola, revólver, escopeta, carabina, rifle, subfusil, fusil): no se desgastan, pero cada disparo atrae zombis en un radio de 150 m. El silenciador amortigua algunos disparos de pistola.</li>
<li><b>Arco y ballesta:</b> casi silenciosos; parte de las flechas vuelve después de la pelea.</li>
<li><b>Lanzables:</b> la botella, la piedra, el despertador y el cohete distraen; la molotov prende fuego al suelo.</li>
</ul>
<p>Recargar con munición en el bolsillo es rápido; si solo está en la mochila, tarda el doble.</p>

<h2>Zombis distintos</h2>
<p>Además del común, hay zombis de uniforme: el <b>presidiario</b> es rápido, el <b>militar</b> y el <b>bombero</b> aguantan mucho (el bombero no se prende fuego), el <b>policía</b> tiene chaleco, el <b>mochilero</b> lleva más cosas. El <b>Bruto</b> es enorme, lento y aguanta seis veces más.</p>

<h2>Salir de la pelea</h2>
<ul>
<li>El ícono de la puerta (<kbd>Salir</kbd>) aparece cuando nadie está a menos de 10 m y nadie te persigue.</li>
<li>Mantente a 40 m de todos los que te vieron durante algunos segundos y te pierden.</li>
<li>O corre hacia el borde rojo de la escena.</li>
</ul>
<div class="tip"><b>Otros sobrevivientes</b>Quien esté cerca de ti en el mundo real aparece en la misma escena, y el mapa avisa cuando alguien está peleando cerca.</div>
"""

BODY["saude"] = """
<p>El cuerpo de tu sobreviviente funciona como un cuerpo. Cada golpe de zombi puede volverse una herida en una parte del cuerpo, y cada herida tiene su tratamiento. Todo está en <b>Personaje → Salud</b>.</p>

<h2>Heridas</h2>
<ul>
<li><b>Arañazo:</b> sangra poco, cierra en 1 día.</li>
<li><b>Laceración:</b> sangra más, 3 días. A veces se vuelve <b>hemorragia</b>, que sangra muy rápido.</li>
<li><b>Mordida:</b> sangra y casi siempre se infecta.</li>
<li><b>Corte profundo:</b> necesita sutura.</li>
<li><b>Esquirla:</b> del vidrio al registrar; sácala con pinzas.</li>
<li><b>Fractura:</b> necesita férula, 7 días.</li>
<li><b>Quemadura:</b> pomada y venda.</li>
</ul>

<h2>Tratar paso a paso</h2>
<ol class="steps">
<li><b>Torniquete</b> (hemorragia): detén la sangre con torniquete o trapo. No lo dejes más de 2 horas sin suturar.</li>
<li><b>Limpiar y desinfectar:</b> suero, alcohol o cachaza.</li>
<li><b>Sacar la esquirla</b> con pinzas, cuando la haya.</li>
<li><b>Suturar</b> con kit de sutura (cortes profundos y hemorragias).</li>
<li><b>Vendar:</b> venda, gasa, vendaje o trapo.</li>
</ol>
<p>La herida solo cicatriza con todos los pasos hechos. Las curaciones se ensucian después de 12 horas (24 con esparadrapo) y hay que cambiarlas; el trapo ya cuenta como sucio. Una herida sucia se infecta, y la infección común se cura con antibiótico.</p>

<h2>La infección zombi</h2>
<div class="tip warn"><b>No tiene cura</b>Una mordida infecta casi siempre; la laceración y el arañazo, a veces. La infección corre en tiempo real: algunos días sin nada, después fiebre, después delirio, y en 7 días el personaje muere.</div>

<h2>Hambre y sed</h2>
<p>El personaje gasta comida y agua como una persona, y más cuando camina. Los avisos aparecen en tres niveles ("Con hambre", "Hambriento", "Enfermo de hambre"). Solo en el último nivel pierde vida, y solo durante la sesión: con la app cerrada nadie muere de hambre.</p>
<p>La comida cocida rinde más y dura más. Para cocinar, enciende una fogata o la cocina de leña (encendedor y tabla). El agua de lluvia puede dar náuseas: hiérvela antes.</p>

<h2>Frío y calor</h2>
<p>La temperatura es la de tu ciudad ahora. Con lluvia sin impermeable y de noche hace más frío; por debajo de 16 °C necesitas ropa abrigada. Con calor, la ropa pesada cansa y la gorra ayuda. El frío gasta comida; el calor gasta agua.</p>

<h2>Cansancio y sueño</h2>
<p>Caminar, correr y pelear cansan. Terminar la sesión con <kbd>Dormir</kbd> en la base, en un puesto o en una tienda de campaña recupera el cansancio y la vida mientras estás fuera. Con cama en la base el descanso es mucho mejor; fuera de ella, el saco de dormir ayuda.</p>

<h2>La cabeza también</h2>
<p>El pánico en la pelea quita precisión; empujar lo alivia. Quedarse mucho tiempo quieto en la base aburre al personaje, y pasar por muchas cosas malas lo entristece. Salir a caminar ayuda.</p>

<h2>Ropa</h2>
<p>La ropa protege la parte del cuerpo que cubre. La ropa rasgada protege a medias: cósela con aguja, hilo y un trapo.</p>

<h2>Cuando muere</h2>
<p>El personaje y sus habilidades se van. Todo lo que llevaba queda en una pila donde cayó: durante 24 horas solo tú la ves, después cualquiera, y un zombi con su rostro la vigila. La cartera pierde el 15% de los sellos. La base, los cofres, el depósito de la radio y la ropa del armario se quedan. Toca <kbd>Nuevo sobreviviente</kbd> y vuelve a la calle.</p>
"""

BODY["base"] = """
<p>La base es el lugar donde guardas lo que juntaste, duermes y cocinas. Cada noche los muertos golpean las paredes.</p>

<h2>Delimitar</h2>
<ol class="steps">
<li>Con la sesión activa, abre el menú de la base y toca <kbd>Delimitar base</kbd>.</li>
<li>Toca la cuadrícula para marcar las esquinas (hasta 60 m de ti). Toca de nuevo la primera esquina para cerrar.</li>
<li>Toca <kbd>Delimitar base</kbd> para confirmar.</li>
</ol>
<p>Empieza con 50 m², y crece con kits de expansión y con gente en el grupo. Tiene que estar a por lo menos 30 m de otra base.</p>
<div class="tip warn"><b>Privacidad</b>La base es visible para quien pasa cerca. No delimites la base donde vives. En casa, usa un puesto avanzado.</div>

<h2>Paredes, puertas y ventanas</h2>
<ul>
<li>Las paredes de edificio son gratis y no caen.</li>
<li>Tus paredes: 1 tabla y 1 clavo cada 4 m. Se pueden reforzar con chapa y después con concreto.</li>
<li>Puerta: 3 tablas y 2 clavos. Ventana: 2 tablas y 1 clavo (las tablas clavadas refuerzan).</li>
<li><kbd>Reparar la pared más débil</kbd> gasta 1 tabla y 1 clavo.</li>
</ul>
<p>Puerta abierta o pared caída = base abierta.</p>

<h2>Muebles</h2>
<p>En la pantalla de acción, dentro de la base, usa el martillo para armar y <kbd>USAR</kbd> para usar:</p>
<ul>
<li><b>Cofre:</b> 40 kg cada uno. Nada entra solo: guárdalo tú.</li>
<li><b>Banco de trabajo:</b> recetas y reparaciones.</li>
<li><b>Cama:</b> descanso mucho mejor. <b>Camilla:</b> las heridas tratadas cicatrizan más rápido.</li>
<li><b>Mesa</b>, <b>fogata</b> (luz y ruido de noche), <b>cocina de leña</b> (casi sin luz).</li>
<li><b>Barril de lluvia:</b> junta agua cuando llueve de verdad.</li>
<li><b>Torre de vigía:</b> ves más lejos cerca de la base. <b>Reflector:</b> necesita generador y gasolina.</li>
<li><b>Buzón:</b> el mercado (mira la guía de grupo).</li>
</ul>

<h2>Huerto</h2>
<p>Hasta 4 huertos: <kbd>Plantar</kbd> las semillas, <kbd>Regar</kbd> (cada riego dura un día) y <kbd>Cosechar</kbd> después de unos 3 días regados.</p>

<h2>Trampas</h2>
<ul>
<li><b>Estacas</b> y <b>pozo cubierto:</b> atrapan atacantes y hay que rearmarlas.</li>
<li><b>Alambre con latas:</b> alarma que avisa y reduce el daño.</li>
</ul>

<h2>El ataque de cada noche</h2>
<p>A la 1 de la madrugada la base es atacada, incluso con la app cerrada (hasta 3 noches perdidas se resuelven cuando vuelves). Paredes más grandes, fogata encendida y reflector prendido atraen a más. Las trampas atrapan a algunos; los demás golpean las paredes, puertas y ventanas.</p>
<p>Si alguna pared cae o una puerta queda abierta, los cofres pierden parte de lo que tienen adentro (la ropa se queda). La horda de la semana también pasa por la base si la ruta llega cerca.</p>
<div class="tip"><b>Estar ahí ayuda</b>Si estás en la base con la sesión activa, el daño baja a la mitad.</div>

<h2>El depósito de la radio y los puestos</h2>
<p>El depósito de la radio es solo tuyo, con 300 kg, y llegas a él desde cualquier puesto avanzado o tienda de campaña. Ahí están el depósito, el banco de trabajo, la radio para volver a la base, el buzón (mercado y almacén), el armario de ropa y la estante de memorias. La ropa del armario se queda incluso después de la muerte.</p>
<p>Puedes tener hasta 10 puestos avanzados, entre 200 m y 20 km de la base y a 100 m unos de otros. El primero es gratis; los demás piden una radio de puesto avanzado.</p>
"""

BODY["grupo"] = """
<h2>Grupo</h2>
<p>En el ícono <kbd>Grupo</kbd>, crea un grupo o entra en uno con el código. Hasta 10 personas.</p>
<ul>
<li>Avisos rápidos en el mapa: <kbd>HORDA AQUÍ</kbd>, <kbd>BOTÍN AQUÍ</kbd> y <kbd>¡AUXILIO!</kbd>.</li>
<li>Chat del grupo, e intercambio de objetos lado a lado.</li>
<li>Una base solo para el grupo, con cofres compartidos. Al entrar en un grupo, tu base se desmonta y lo que tenía va al depósito de la radio.</li>
<li>Los roles en el grupo dan más experiencia: <b>Médico</b>, <b>Constructor</b> y <b>Explorador</b>.</li>
</ul>
<p>Nadie fuera del grupo ve tu nombre. Para intercambiar con cualquier persona cerca (hasta 40 m), usa <kbd>Intercambiar con alguien aquí</kbd> en el menú.</p>

<h2>Sellos y mercado</h2>
<p>La moneda del apocalipsis es el <b>sello</b>. El mercado de todo el mundo está en el <b>buzón</b> de la base o del depósito de la radio:</p>
<ul>
<li><kbd>Mercado</kbd>: compra y vende con otros sobrevivientes. Tienes 6 espacios; poner una oferta cuesta 1 sello y quien vende paga una pequeña comisión. Nadie ve lo que negocian los demás, solo el precio de referencia.</li>
<li><kbd>Almacén</kbd>: el mostrador vende lo básico y compra cualquier cosa barato, y funciona incluso sin internet.</li>
</ul>
<p>Los sellos que pasan mucho tiempo quietos por encima de 300 pierden un poco cada semana. Morir cuesta el 15% de ellos.</p>

<h2>Bastiones</h2>
<p>Los lugares grandes (salud, mercado, restaurante, construcción, gasolinera, policía, bomberos, escuela) tienen bandera. Toca <kbd>Tomar el bastión</kbd> y vence a quienes están ahí en una arena con autos y barricadas: al principio son bandidos, muchos armados.</p>
<p>Si ganas, el bastión es tuyo (o del grupo) y paga 4 sellos por día. Deja hasta 6 guardias: cada uno se lleva un arma tuya (y la munición). El guardia que cae desaparece con el arma. Sin guardias, cualquiera lo toma sin pelear.</p>

<h2>Bengalas de rescate</h2>
<p>Enciende una bengala y aguanta las oleadas: fácil (3), media (4) o difícil (5, con el Bruto al final). Si ganas, cae una caja de rescate y tienes 30 minutos para tomar lo que puedas.</p>
"""

BODY["corvo"] = """
<h2>El cuervo</h2>
<p>Cuando pones la primera puerta en la base, un cuervo se posa en ella. Se queda. Solo tú lo ves.</p>
<ul>
<li><b>Avisa de la horda:</b> cuando muchos zombis vienen tras de ti, llega volando desde esa dirección, graznando.</li>
<li><b>Muestra cuerpos:</b> rodea las pilas de cuerpos que aún no se registraron.</li>
<li><b>Un lugar por día:</b> se posa en un lugar sin saquear cercano que gana un objeto raro extra.</li>
<li>Vuela desde la dirección de los avisos de tu grupo, y huye del ruido fuerte.</li>
</ul>
<p>En el botón <kbd>Cuervo</kbd> del mapa, dale comida para crear un vínculo. Con más confianza lleva cosas livianas al depósito, señala zombis especiales, trae un objeto pequeño del depósito y, en el último nivel, grazna para distraer hasta 3 zombis por un rato. Con hambre, no vuela.</p>

<h2>Radio Cuervo</h2>
<p>Con una radio en la mochila, en los cofres o en el depósito, abre el menú → <kbd>Radio</kbd>:</p>
<ul>
<li><b>La horda de la semana:</b> anunciada desde el lunes, de 30 a 60 zombis que vienen de una dirección, en una noche entre miércoles y domingo. Atraviesa la región en línea recta, y la radio dice si pasa cerca de tu base.</li>
<li><b>Cajas de suministros:</b> 2 por semana en la región, de día. Duran 24 horas y su ruido atrae zombis por un rato. Sin radio, solo te enteras de las que están muy cerca.</li>
<li><b>Pista del día:</b> un lugar sin saquear con un objeto raro extra.</li>
<li><b>Misión de la semana:</b> abatir, saquear, caminar o guardar tablas, y ganar sellos.</li>
<li>La frase del día, y alarmas que suenan por la ciudad y atraen a los zombis.</li>
</ul>

<h2>Clima y hora reales</h2>
<ul>
<li><b>Lluvia:</b> amortigua tu ruido, acorta la vista, enfría y llena el barril.</li>
<li><b>Niebla:</b> acorta mucho la vista.</li>
<li><b>Tormenta:</b> amortigua más el ruido, pero deja a los zombis agitados.</li>
<li><b>Noche:</b> empieza con la puesta de sol real. De madrugada se agitan y oyen mejor.</li>
<li><b>Luna llena:</b> ves más lejos de noche, pero ellos también, y salen a caminar más de ellos.</li>
</ul>
"""

BODY["memorias"] = """
<p>Por la ciudad hay libros raros que guardan los últimos días de quienes vinieron antes. Cada uno es una <b>memoria</b>: una historia jugable, con principio, desarrollo y final, y una prenda de recompensa.</p>

<h2>Dónde encontrarlas</h2>
<p>Los libros (<i>Memoria: …</i>) son legendarios y aparecen muy raramente en los muebles <b>de adentro</b> de los lugares: solo entrando, nunca por la puerta. Cada memoria sale de un tipo de lugar:</p>
<ul>
<li><b>Don Jorge:</b> casas</li>
<li><b>La guardia:</b> lugares de salud</li>
<li><b>La voz del cuervo:</b> tiendas de electrónica</li>
<li><b>Guardia del jueves:</b> comisarías</li>
<li><b>La bóveda:</b> búnkeres militares</li>
</ul>
<p>Quien ya leyó un libro no encuentra otro igual. Si encuentras uno repetido, se convierte en 3 sellos.</p>

<h2>Jugar</h2>
<ol class="steps">
<li>En la mochila, toca el libro y luego <kbd>Poner en la estantería</kbd>.</li>
<li>Ve a un puesto avanzado o tienda de campaña y entra en el depósito de la radio.</li>
<li>Abre la <kbd>ESTANTE DE MEMORIAS</kbd>, toca el lomo y luego <kbd>JUGAR</kbd>. La sesión se termina para que empiece la memoria.</li>
</ol>
<p>En la memoria juegas con otra persona, con su kit; tu personaje queda guardado y nada de lo que pasa ahí lo afecta. Si caes antes del final, la memoria falló: vuelve a empezar <kbd>DESDE AQUÍ</kbd> o <kbd>DESDE EL INICIO</kbd>. La estante guarda tu récord de abatidos.</p>

<h2>Las siete memorias</h2>
<ul>
<li><b>La última entrega:</b> el cartero en la noche de la tormenta. Uniforme del Cartero.</li>
<li><b>Don Jorge:</b> el portero que cerró el edificio. Ropa de Portero.</li>
<li><b>La guardia:</b> la enfermera Lúcia en su última guardia de urgencias. Ropa de Enfermera.</li>
<li><b>La voz del cuervo:</b> la locutora Rosa, que no salió del aire. Auriculares de locutora, y la frase del día de la radio pasa a llevar su firma.</li>
<li><b>Guardia del jueves:</b> el soldado Ramos defendiendo la comisaría. Uniforme de Policía.</li>
<li><b>La bóveda:</b> el soldado Nunes bajando el búnker piso por piso. Uniforme Militar.</li>
<li><b>El cuervo:</b> solo volar y leer. Aparece en la estante después de jugar las otras seis.</li>
</ul>
<div class="tip"><b>Cintas en la pata</b>Al terminar El cuervo, tu cuervo pasa a llevar una cinta de cada memoria.</div>
"""
