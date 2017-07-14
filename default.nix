# -*- mode: nix -*-
{ pkgs ? import ./nix/pinned-pkgs.nix { } }:

with pkgs; python3Packages.buildPythonPackage rec {
  pname = "";
  version = "0.1.0";
  name = "${pname}-${version}";

  src = ./.;

  # The checkInputs attribute is cleared or deleted or something by
  # buildPythonPackage, so we need a dummy attribute to reference from shell.nix.
  check_inputs = [ ];
  checkInputs = check_inputs;

  propagatedBuildInputs = with python3Packages; [
    docker
  ];

  meta = with lib; {
    homepage = https://github.com/siddharthist/computational-homology;
    description = "";
    maintainers = with maintainers; [ siddharthist ];
    platforms = platforms.linux;
  };
}
