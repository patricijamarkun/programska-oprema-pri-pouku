# Pregled snovi: zaporedja

## 1. Kaj je zaporedje?

**Zaporedje** je urejen seznam števil, pri katerem je vsakemu naravnemu številu $n$ prirejen člen $a_n$. Člene označujemo z $a_1, a_2, a_3, \ldots$, kjer je $a_1$ prvi člen, $a_n$ pa splošni člen.

Zaporedje lahko podamo:

- **z naštevanjem členov**, na primer $2, 5, 8, 11, \ldots$;
- **s splošnim členom**, na primer $a_n=3n-1$;
- **rekurzivno**, tako da določimo začetni člen in pravilo za izračun naslednjega, na primer $a_1=2$ in $a_{n+1}=a_n+3$.

## 2. Aritmetično zaporedje

Zaporedje je **aritmetično**, kadar je razlika med zaporednima členoma vedno enaka. To stalno razliko imenujemo **diferenca** $d$:

$$d=a_{n+1}-a_n.$$

Splošni člen in vsota prvih $n$ členov:

$$a_n=a_1+(n-1)d, \qquad S_n=\frac{n(a_1+a_n)}{2}.$$

**Primer:** Zaporedje $4, 7, 10, 13, \ldots$ ima $a_1=4$ in $d=3$. Zato je $a_n=4+3(n-1)=3n+1$. Deseti člen je $a_{10}=31$, vsota prvih desetih členov pa $S_{10}=\frac{10(4+31)}2=175$.

## 3. Geometrijsko zaporedje

Zaporedje je **geometrijsko**, kadar je količnik zaporednih členov vedno enak. Ta stalni količnik imenujemo **kvocient** $q$:

$$q=\frac{a_{n+1}}{a_n} \quad (a_n\ne 0).$$

Splošni člen in vsota prvih $n$ členov:

$$a_n=a_1q^{n-1}, \qquad S_n=a_1\frac{1-q^n}{1-q} \quad (q\ne1).$$

Če je $q=1$, je $S_n=na_1$. Vsota neskončnega geometrijskega zaporedja obstaja, kadar je $|q|<1$:

$$S_\infty=\frac{a_1}{1-q}.$$

**Primer:** Zaporedje $3, 6, 12, 24, \ldots$ ima $a_1=3$ in $q=2$. Peti člen je $a_5=3\cdot2^4=48$, vsota prvih petih členov pa $S_5=3\frac{1-2^5}{1-2}=93$.

## 4. Kako rešujemo naloge?

1. Iz podatkov določi prvi člen $a_1$ in preveri, ali je zaporedje aritmetično (stalna razlika) ali geometrijsko (stalni količnik).
2. Zapiši ustrezno formulo za $a_n$ oziroma $S_n$.
3. Vstavi znane podatke in izračunaj iskano vrednost. Pri vsoti preveri, ali iščeš vsoto končnega ali neskončnega zaporedja.
4. Smiselno preveri rezultat, na primer tako, da iz splošnega člena izračunaš nekaj začetnih členov.

**Primer določanja splošnega člena:** Aritmetično zaporedje ima $a_1=5$ in $d=-2$. Potem je

$$a_n=5+(n-1)(-2)=7-2n.$$

## Na kratko

- Aritmetično: prištevamo isto število $d$.
- Geometrijsko: množimo z istim številom $q$.
- Splošni člen pove, kako neposredno izračunamo člen na mestu $n$.
- Vsota $S_n$ pomeni vsoto prvih $n$ členov.
