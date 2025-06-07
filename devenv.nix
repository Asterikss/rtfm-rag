{
  pkgs,
  lib,
  config,
  inputs,
  ...
}:

let
  buildInputs = with pkgs; [
    stdenv.cc.cc
    libuv
    zlib
  ];
  AtlasVersion = "0.34.0";
in
{
  env = {
    LD_LIBRARY_PATH = "${with pkgs; lib.makeLibraryPath buildInputs}";
  };

  languages.python = {
    enable = true;
    version = "3.11";
    uv = {
      enable = true;
      sync.enable = true;
    };
  };

  overlays = [
    (final: prev: {
      atlas = prev.atlas.overrideAttrs (oldAttrs: rec {
        version = AtlasVersion;

        src = prev.fetchFromGitHub {
          owner = "ariga";
          repo = "atlas";
          rev = "v${version}";
          hash = "sha256-7s03YrZw7J2LRCHibMqzBBtVUBSPVEf+TMqtKoWSkkM=";
        };

        vendorHash = "sha256-K94zOisolCplE/cFrWmv4/MWl5DD27lRekPTl+o4Jwk=";
      });
    })
  ];

  dotenv.disableHint = true;

  scripts.run.exec = ''
    uvicorn src.main:app --reload --port 8032
  '';

  scripts.run-prod.exec = ''
    uvicorn src.main:app --port 8032
  '';

  packages = [
    pkgs.atlas
  ];
  services.postgres = {
    enable = true;
    listen_addresses = "localhost";
    port = 5432;
    initialDatabases = [ { name = "rtfm-rag"; } ];
    extensions = extensions: [
      extensions.pgvector
    ];
  };
}
