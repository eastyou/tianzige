"""支持 ``python -m tianzige``。"""

from .cli import main

if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
