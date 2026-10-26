# Repository GitHub Emilianowv/Occidentale

Il repository locale usa `main` e il remote `https://github.com/Emilianowv/Occidentale.git`. L'autore è `Emilianowv` e l'indirizzo dei commit è il GitHub noreply associato al suo ID pubblico:

```bash
git config --local user.name Emilianowv
git config --local user.email 309815527+Emilianowv@users.noreply.github.com
```

Questi comandi configurano soltanto questo repository. Non usare l'indirizzo Git globale personale. `scripts/audit.py` impedisce altri indirizzi nei file distribuiti e non include home, snapshot, configurazioni Git o credenziali.

## Creazione e primo invio

Creare su GitHub un repository vuoto chiamato **Occidentale** nell'account **Emilianowv**, senza README o licenza generati. La scelta pubblico/privato appartiene al proprietario; questa preparazione locale non cambia la visibilità di altri progetti. Poi, con Git autenticato come Emilianowv:

```bash
git remote -v
git log -1 --format=fuller
make check
make build
python3 scripts/test_deb.py
git push -u origin main
```

Se `gh` è collegato a un altro account, autenticarsi come Emilianowv prima di usarlo per creare il repository. Il connettore GitHub dell'app e il client `gh` possono avere account e autorizzazioni differenti. Non copiare token nei file del progetto.

## Release

`check.yml` verifica Debian 13 e produce gli artifact. `release.yml` controlla il tag rispetto a `VERSION`, ricostruisce e prova il pacchetto in un container Debian 13 e crea una **bozza** di release:

```bash
git tag v6.1.0
git push origin v6.1.0
```

Rivedere la bozza, i checksum e le note prima di pubblicarla. Il workflow richiede le normali autorizzazioni di GitHub Actions per creare una release; non contiene token personali. I job remoti sono preparati, ma un esito locale non viene presentato come esecuzione remota già completata.

File da allegare: `Occidentale-6.1.0.zip`, `Occidentale-6.1.0.tar.gz`, `occidentale_6.1.0_all.deb`, `SHA256SUMS`. I primi due sono archivi del sorgente con installatore, test, documentazione e bozza Windows; l'unico pacchetto binario installabile prodotto è il `.deb` indipendente dall'architettura.

Il file COPYRIGHT mantiene lo stato dei diritti del sorgente ricevuto. Non viene attribuita automaticamente una licenza open source al lavoro originale.
