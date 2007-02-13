Summary:	A game like "Deflektor" or "Mindbender"
Summary(pl.UTF-8):	Gra podobna do Deflektora lub Mindbendera
Summary(pt_BR.UTF-8):	Jogo de refletir raios para X, tipo "Mindbender" ou "Deflektor"
Name:		mirrormagic
Version:	2.0.2
Release:	1
License:	GPL
Group:		X11/Applications/Games
Source0:	http://www.artsoft.org/RELEASES/unix/mirrormagic/%{name}-%{version}.tar.gz
# Source0-md5:	32fd3909c1e27f493d89bc2276da6744
Source1:	%{name}.desktop
Source2:	%{name}.png
Patch0:		%{name}-va_arg.patch
URL:		http://www.artsoft.org/mirrormagic/
BuildRequires:	SDL_image-devel
BuildRequires:	SDL_mixer-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)


%description
Mirror Magic is an arcade style game for X, like "Mindbender" (Amiga)
or "Deflektor" (Atari ST). It was first released 1989 on the Amiga.

Your task is to get all the 'magic kettles' which contain 'magic spell
ingredients', hitting them with the 'magic beam' that starts from the
magician. The gnomes each have a mirror which can be rotated by
clicking with the left or right mouse button, so you can reflect the
'magic beam' to another direction. If you have gotten all the 'magic
kettles', the 'magic door' opens and you only have to direct the
'magic beam' to this door to end the level.

To complicate the game, the following levels will contain more and
more of some strange elements to help you in the level or to make it
harder. Just try out what they do when you see them in a new level -
you will quickly find it out... :)

%description -l pl.UTF-8
Mirror Magic jest grą zręcznościową dla X, podobną do Mindbendera
(Amiga) lub Deflektora (Atari ST). Pierwsza wersja ukazała się na
Amigę w 1989 roku.

Twoim zadaniem jest zebranie wszystkich magicznych kociołków, które
zawierają składniki zaklęcia, poprzez trafienie ich magicznym
promieniem, który emitowany jest przez magika. Gnomy trzymają lustra,
które odbijają promień w innym kierunku. Gdy zbierzesz wszystkie
magiczne kociołki, otworzą się magiczne drzwi, do których trzeba
trafić promieniem by zakończyć poziom.

By skomplikować grę, późniejsze poziomy zawierają coraz więcej
dziwnych elementów, pomagających Ci, lub przeszkadzających. Sprawdź co
robią, gdy je zobaczysz - szybko się przekonasz... :)

%description -l pt_BR.UTF-8
O Mirror Magic é um jogo do estilo arcade para X, tipo o "Mindbender"
(Amiga) ou o "Deflektor" (Atari ST). Ele foi lançado em 1989 para o
Amiga.

Sua missão é acertar todos os 'potes mágicos' que contêm 'ingredientes
para feitiços mágicos' batendo neles com o 'raio mágico' que vem do
mago. Cada gnomo tem um espelho que pode ser rotacionado clicando nos
botões do mouse, para refletir o 'raio mágico' para outra direção. Se
você acertou todos os 'potes mágicos', a 'porta mágica' se abrirá e
basta você direcionar o 'raio mágico' a ela para finalizar o nível.

Para complicar o jogo, os níveis seguintes terão mais e mais coisas
estranhas para ajudá-lo ou atrapalhá-lo. Basta tentar usá-los assim
que os vir, você logo descobrirá se são do bem ou do mal :)

%prep
%setup -q
%patch0 -p1

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -DTARGET_SDL `sdl-config --cflags` \
		-DSCORE_ENTRIES=MANY_PER_NAME \
		-DRO_GAME_DIR=\\\"%{_datadir}/games/%{name}\\\" \
		-DRW_GAME_DIR=\\\"/var/games/%{name}\\\"" \
	LDFLAGS="%{rpmldflags} -lSDL_image -lSDL_mixer `sdl-config --libs`"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/games/%{name},%{_pixmapsdir},%{_applnkdir}/Games}

install %{name} $RPM_BUILD_ROOT%{_bindir}
mv -f graphics levels music sounds $RPM_BUILD_ROOT%{_datadir}/games/%{name}

install %{SOURCE1} $RPM_BUILD_ROOT%{_applnkdir}/Games
install %{SOURCE2} $RPM_BUILD_ROOT%{_pixmapsdir}

# scores
install -d $RPM_BUILD_ROOT/var/games/%{name}/scores/
for i in $RPM_BUILD_ROOT%{_datadir}/games/%{name}/levels/*; do
	cd $i
	for j in `find * -type d`; do
		mkdir $RPM_BUILD_ROOT/var/games/%{name}/scores/$j
		cd $j
		for k in `ls | grep \\\.level`; do
			touch $RPM_BUILD_ROOT/var/games/%{name}/scores/$j/`basename $k .level`.score
		done
		cd ..
	done
	cd ..
done

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README CHANGES
%attr(2755,root,games) %{_bindir}/*
%{_datadir}/games/%{name}
%{_pixmapsdir}/*
%{_applnkdir}/Games/*
%defattr(664,root,games,755)
/var/games/%{name}
