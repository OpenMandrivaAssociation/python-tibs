# Rust sucks
%undefine _debugsource_template
%define module tibs

Name:		python-tibs
Version:	0.8.0
Release:	1
Summary:	A sleek Python library for binary data
License:	MIT
Group:		Development/Python
URL:		https://github.com/scott-griffiths/tibs
Source0:	https://github.com/scott-griffiths/tibs/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:	%{name}-%{version}-vendor.tar.xz

BuildSystem:	python
BuildRequires:	cargo
BuildRequires:	pkgconfig(python3)
BuildRequires:	python%{pyver}dist(pip)
BuildRequires:	python%{pyver}dist(maturin)
BuildRequires:	python%{pyver}dist(wheel)
BuildRequires:	rust-packaging

%description
A sleek Python library for binary data.

%prep -a
tar xf %{S:1}
%cargo_prep -v vendor

cat >>.cargo/config <<EOF
[source.crates-io]
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "vendor"
EOF

%build -p
# Rust doesnt accept LDFLAGS, instead we need to use RUSTFLAGS to ensure it
# links properly during compile to fix undefined symbols being reported
# during packaging.
export RUSTFLAGS="-lpython%{pyver}"
export CARGO_HOME=$PWD/.cargo

%build -a
# sort out crate licenses
%cargo_license_summary
%{cargo_license} > LICENSES.dependencies

%files
%license LICENSE LICENSES.dependencies
%{python_sitearch}/%{module}
%{python_sitearch}/%{module}-%{version}.dist-info
