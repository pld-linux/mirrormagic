Summary:	A game like "Deflektor" or "Mindbender"
Summary(pl):	Gra podobna do Deflektora lub Mindbendera
Name:		mirrormagic
Version:	2.0.0
Release:	1
License:	GPL
Group:		X11/Applications/Games
Source0:	http://www.artsoft.org/RELEASES/unix/mirrormagic/%{name}-%{version}.tar.gz
Source1:	%{name}.desktop
Source2:	%{name}.png
URL:		http://www.artsoft.org/mirrormagic/
BuildRequires:	SDL-devel >= 1.1.0
BuildRequires:	SDL_image-devel
BuildRequires:	SDL_mixer-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr/X11R6
%define		_mandir		%{_prefix}/man

%description
This is a port of a game I wrote for the Amiga in 1989. Included are
many levels known from the games "Deflektor" and "Mindbender"

%description -l pl
To jest port gry z Amigi z 1989 roku. Za³±czone jest wiele poziomów
znanych z gier Deflektor i Mindbender.

%prep
%setup -q

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

gzip -9nf README CHANGES

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
%doc *.gz
%attr(2755,root,games) %{_bindir}/*
%{_datadir}/games/%{name}
%{_pixmapsdir}/*
%{_applnkdir}/Games/*
%defattr(664,root,games,755)
/var/games/%{name}
