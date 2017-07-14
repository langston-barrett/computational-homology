{ pkgs ? import <nixpkgs> { } }:

import (pkgs.fetchFromGitHub {
  owner  = "NixOS";
  repo   = "nixpkgs";
  rev    = "17.03";
  sha256 = "1fw9ryrz1qzbaxnjqqf91yxk1pb9hgci0z0pzw53f675almmv9q2";
}) { }
