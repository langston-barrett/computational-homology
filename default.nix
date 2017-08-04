# -*- mode: nix -*-
{ pkgs ? import ./nix/pinned-pkgs.nix { } }:

with pkgs; python27Packages.buildPythonPackage rec {
  pname = "computational-homology";
  version = "0.1.0";
  name = "${pname}-${version}";

  src = if lib.inNixShell then null else ./.;

  meta = with lib; {
    homepage = https://github.com/siddharthist/computational-homology;
    description = "See README";
    maintainers = with maintainers; [ siddharthist ];
    platforms = platforms.linux;
  };
}
