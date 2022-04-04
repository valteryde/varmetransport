# varmetransport
Varmetranport for SRP opgave FY/If 2022

---
## Guide til brug af programmet varmetransport
*I zip-filen gemmer der sig 2 mapper: Build og src.*

### Mappen ”src”
Src er mappen hvor alt ”source coden” gemmer sig. Hvis man ønsker at køre programmet manuelt, kan man åbne terminalen og give det et forsøg med kommandoen
      '>>>python main.py'
Hvis man blot ønsker at se indholdet, kan man åbne filen i en tekst redigerings program og opdage hvordan programmet virker. De anvendte værktøjer er: Python på bagsiden, javascript på frontsiden. Kommunikationen imellem de to sker ved http og sockets. GUI’en (Brugerfladen) anvender en ”webrender” ligesom chrome, som viser html og css. Derudover så bruges pakken ”pygame” til animation og visning af simuleringen. For 3D plot bruges pakken ”matplotlib”. 

### Mappen ”build”
I denne mappe findes tre filer. Her skal man vælge den der passer til ens styresystem. Bruger man windows skal man bruge ”varmetransport_windows.zip”. Når man har ”åbnet” zip-filen skal man navigere hen til filen main.exe (Kan også bare hedde ”main”). Denne skal man bare trykke på. NB: Windows versionen er en demo version og har dermed et mindre udvalg af funktioner. Bruger man derimod MacOS, altså Apples styresystem, så har man to muligheder. Enten kan man åbne programmet varmetransport, hvoraf programmet burde starte. Eller så kan man ”åbne” zip-filen varmetransport_darwin.zip, hvoraf man derefter skal åbne programmet varmetransport.

### Fejlfinding
Skulle der, imod forventning, ske en fejl så kan man oprette en fejlrapport på https://github.com/valteryde/varmetransport/issues eller sende en mail til valteryde@hotmail.com. Det første man også burde gøre, er at værne med tålmodighed. Programmet er langsomt, specielt på Windows. En genstart er også altid en god ide. Har man dog python installeret kan man med fordel køre programmet i en terminal/kommandoprompt. Programmet er lavet på MacOS styresystemet (MacOS Big Sur v11.5.2), hvilket gør at det er bedst testet og optimeret til dette styresystem. Dette betyder at, hvis der skulle ske en fejl på windows så kan man med fordel prøve programmet på en Mac. Hvis man har sådan en i besiddelse.

Slår alt dog fejl og computeren står i brand, så er der lavet en video gennemgang af programmet som kan ses her  https://youtu.be/STLsDJUf8SM. 

---
Valter Yde Daugberg
