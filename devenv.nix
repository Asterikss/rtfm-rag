{
  pkgs,
  lib,
  config,
  inputs,
  ...
}:

{
  languages.python = {
    enable = true;
    version = "3.11";
    uv = {
      enable = true;
      sync.enable = true;
    };
  };
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
