Summary:	A game like "Deflektor" or "Mindbender"
Summary(pl):	Gra podobna do Deflektora lub Mindbendera
Summary(pt_BR):	Jogo de refletir raios para X, tipo "Mindbender" ou "Deflektor"
Name:		mirrormagic
Version:	2.0.1
Release:	2
License:	GPL
Group:		X11/Applications/Games
Source0:	http://www.artsoft.org/RELEASES/unix/mirrormagic/%{name}-%{version}.tar.gz
Source1:	%{name}.desktop
Source2:	%{name}.png
Patch0:		%{name}-va_arg.patch
URL:		http://www.artsoft.org/mirrormagic/
BuildRequires:	SDL_image-devel
BuildRequires:	SDL_mixer-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr/X11R6
%define		_mandir		%{_prefix}/man

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

%description -l pl
Mirror Magic jest gr� zr�czno�ciow� dla X, podobn� do Mindbendera
(Amiga) lub Deflektora (Atari ST). Pierwsza wersja ukaza�a si� na
Amig� w 1989 roku.

Twoim zadaniem jest zebranie wszystkich magicznych kocio�k�w, kt�re
zawieraj� sk�adniki zakl�cia, poprzez trafienie ich magicznym
promieniem, kt�ry emitowany jest przez magika. Gnomy trzymaj� lustra,
kt�re odbijaj� promie� w innym kierunku. Gdy zbierzesz wszystkie
magiczne kocio�ki, otworz� si� magiczne drzwi, do kt�rych trzeba
trafi� promieniem by zako�czy� poziom.

By skomplikowa� gr�, p�niejsze poziomy zawieraj� coraz wi�cej
dziwnych element�w, pomagaj�cych Ci, lub przeszkadzaj�cych. Sprawd� co
robi�, gdy je zobaczysz - szybko si� przekonasz... :)

%description -l pt_BR
O Mirror Magic � um jogo do estilo arcade para X, tipo o "Mindbender"
(Amiga) ou o "Deflektor" (Atari ST). Ele foi lan�ado em 1989 para o
Amiga.

Sua miss�o � acertar todos os 'potes m�gicos' que cont�m 'ingredientes
para feiti�os m�gicos' batendo neles com o 'raio m�gico' que vem do
mago. Cada gnomo tem um espelho que pode ser rotacionado clicando nos
bot�es do mouse, para refletir o 'raio m�gico' para outra dire��o. Se
voc� acertou todos os 'potes m�gicos', a 'porta m�gica' se abrir� e
basta voc� direcionar o 'raio m�gico' a ela para finalizar o n�vel.

Para complicar o jogo, os n�veis seguintes ter�o mais e mais coisas
estranhas para ajud�-lo ou atrapalh�-lo. Basta tentar us�-los assim
que os vir, voc� logo descobrir� se s�o do bem ou do mal :)

%prep
%setup -q
%patch0 -p1

%build
%{__make} \
	CC=%{__cc} \
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
for i in $RPM_BUILD_ROOT%{_datadir}/games/%{name}/levels/*
do
        cd $i
        for j in `find * -type d`
        do
                mkdir $RPM_BUILD_ROOT/var/games/%{name}/scores/$j
                cd $j
                for k in `ls | grep \\\.level`
                do
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
