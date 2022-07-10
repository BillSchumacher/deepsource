import sys

__all__ = ('main',)


def main() -> None:
    from deepsource.bin.deepsource import main as _main
    sys.exit(_main())


if __name__ == '__main__':  # pragma: no cover
    main()
