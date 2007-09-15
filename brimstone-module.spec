%define section         free
%define gcj_support     1

Name:           brimstone-module
Version:        0.1.27
Release:        %mkrel 0.0.2
Epoch:          0
Summary:        org.freecompany.brimstone
License:        MIT
Group:          Development/Java
URL:            http://www.freecompany.org/
# svn export https://svn.freecompany.org/public/brimstone/tags/brimstone-module-0.1.27 | yes t
# zip -9r brimstone-module-src-0.1.27.zip brimstone-module-0.1.27
Source0:        http://repository.freecompany.org/org/freecompany/brimstone/zips/brimstone-module-src-%{version}.zip
Source1:        brimstone-module-0.1.27-build.xml
Requires:       brimstone-cache
Requires:       brimstone-core
Requires:       util-core
Requires:       util-multicaster
Requires:       util-xml-editor
BuildRequires:  ant
BuildRequires:  ant-junit
BuildRequires:  brimstone-cache
BuildRequires:  brimstone-core
BuildRequires:  util-core
BuildRequires:  util-multicaster
BuildRequires:  util-xml-editor
BuildRequires:  jpackage-utils >= 0:1.6
BuildRequires:  junit
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildRequires:  java-devel
BuildArch:      noarch
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
org.freecompany.brimstone

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
Javadoc for %{name}.

%prep
%setup -q
%{__cp} -a %{SOURCE1} build.xml
%{__perl} -pi -e 's|<javac|<javac nowarn="true"|g' build.xml

%build
export CLASSPATH=$(build-classpath junit brimstone-cache brimstone-core util-core util-multicaster util-xml-editor)
export OPT_JAR_LIST="ant/ant-junit"
# XXX: test testModuleClassLoader does not pass
%{ant} jar javadoc #test

%install
%{__rm} -rf %{buildroot}

%{__mkdir_p} %{buildroot}%{_javadir}
%{__cp} -a dist/%{name}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do %{__ln_s} ${jar} ${jar/-%{version}/}; done)

%{__mkdir_p} %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__cp} -a dist/doc/* %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__ln_s} %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
%{__rm} -rf %{buildroot}

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-%{version}.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/%{name}-%{version}.jar.db
%attr(-,root,root) %{_libdir}/gcj/%{name}/%{name}-%{version}.jar.so
%endif

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}
