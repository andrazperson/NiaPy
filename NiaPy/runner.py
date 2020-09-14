# encoding=utf8

"""Implementation of Runner module."""

from __future__ import print_function

import datetime
import os
import logging

import pandas as pd

from NiaPy.task import StoppingTask, OptimizationType
from NiaPy.algorithms import AlgorithmUtility

logging.basicConfig()
logger = logging.getLogger('NiaPy.runner.Runner')
logger.setLevel('INFO')

__all__ = ["Runner"]


class Runner:
    r"""Runner utility feature class.

    Feature which enables running multiple algorithms with multiple benchmarks.
    It also support exporting results in various formats (e.g. Pandas DataFrame, JSON, Excel)

    !!!example
        ```python
        from NiaPy import Runner
        from NiaPy.algorithms.basic import (
            GreyWolfOptimizer,
            ParticleSwarmAlgorithm
        )
        from NiaPy.benchmarks import (
            Benchmark,
            Ackley,
            Griewank,
            Sphere,
            HappyCat
        )

        # Initialize Runner with multiple algorithms and/or benchmark functions
        runner = Runner(
            D=40,
            nFES=100,
            nRuns=2,
            useAlgorithms=[
                GreyWolfOptimizer(),
                "FlowerPollinationAlgorithm",
                ParticleSwarmAlgorithm(),
                "HybridBatAlgorithm",
                "SimulatedAnnealing",
                "CuckooSearch"
            ],
            useBenchmarks=[
                Ackley(),
                Griewank(),
                Sphere(),
                HappyCat(),
                "rastrigin"
            ]
        )

        # Run the Runner with export option set to export results to Pandas DataFrame
        runner.run(export='dataframe', verbose=True)

        ```
    """

    def __init__(self, D=10, nFES=1000000, nRuns=1, useAlgorithms='ArtificialBeeColonyAlgorithm', useBenchmarks='Ackley', **kwargs):
        r"""Initialize Runner.

        Args:
            D (int): Dimension of problem
            nFES (int): Number of function evaluations
            nRuns (int): Number of repetitions
            useAlgorithms (List[Algorithm]): List of algorithms to run
            useBenchmarks (List[Benchmarks]): List of benchmarks to run
        """

        self.D = D
        self.nFES = nFES
        self.nRuns = nRuns
        self.useAlgorithms = useAlgorithms
        self.useBenchmarks = useBenchmarks
        self.results = {}

    def benchmark_factory(self, name):
        r"""Create optimization task.

        Args:
            name (str): Benchmark name.

        Returns:
            Task: Optimization task to use.

        """
        return StoppingTask(D=self.D, nFES=self.nFES, optType=OptimizationType.MINIMIZATION, benchmark=name)

    @classmethod
    def __create_export_dir(cls):
        r"""Create export directory if not already createed."""
        if not os.path.exists("export"):
            os.makedirs("export")

    @classmethod
    def __generate_export_name(cls, extension):
        r"""Generate export file name.

        Args:
            extension (str): File format.

        Returns:
            str: Generated export name with postfix based on the passed extension.
        """

        Runner.__create_export_dir()
        return "export/" + str(datetime.datetime.now()).replace(":", ".") + "." + extension

    def __export_to_dataframe_pickle(self):
        r"""Export the results in the pandas dataframe pickle.

        Note: See Also
            * [`__createExportDir`](#NiaPy.runner.Runner._Runner__create_export_dir)
            * [__generateExportName](#NiaPy.runner.Runner._Runner__generate_export_name)

        """

        dataframe = pd.DataFrame.from_dict(self.results)
        dataframe.to_pickle(self.__generate_export_name("pkl"))
        logger.info("Export to Pandas DataFrame pickle (pkl) completed!")

    def __export_to_json(self):
        r"""Export the results in the JSON file.

        Note: See Also
            * [__createExportDir](#NiaPy.runner.Runner._Runner__create_export_dir)
            * [__generateExportName](#NiaPy.runner.Runner._Runner__generate_export_name)

        """

        dataframe = pd.DataFrame.from_dict(self.results)
        dataframe.to_json(self.__generate_export_name("json"))
        logger.info("Export to JSON file completed!")

    def _export_to_xls(self):
        r"""Export the results in the xls file.

        Note: See Also
            * [__createExportDir](#NiaPy.runner.Runner._Runner__create_export_dir)
            * [__generateExportName](#NiaPy.runner.Runner._Runner__generate_export_name)

        """

        dataframe = pd.DataFrame.from_dict(self.results)
        dataframe.to_excel(self.__generate_export_name("xls"))
        logger.info("Export to XLS completed!")

    def __export_to_xlsx(self):
        r"""Export the results in the xlsx file.

        Note: See Also
            * [__createExportDir](#NiaPy.runner.Runner._Runner__create_export_dir)
            * [__generateExportName](#NiaPy.runner.Runner._Runner__generate_export_name)

        """

        dataframe = pd.DataFrame.from_dict(self.results)
        dataframe.to_excel(self.__generate_export_name("xslx"))
        logger.info("Export to XLSX file completed!")

    def run(self, export="dataframe", verbose=False):
        """
        Execute runner.

        Arguments:
            export (str): Takes export type (e.g. dataframe, json, xls, xlsx)
            verbose (bool): Switch for verbose logging (default: {False})

        Raises:
            TypeError: Raises TypeError if export type is not supported

        Returns:
            results (Dict[str, Dict]): Returns the results.

        Note: See Also
            * [benchmark_factory](#NiaPy.runner.Runner.benchmark_factory)
        """

        for alg in self.useAlgorithms:
            if not isinstance(alg, "".__class__):
                alg_name = str(type(alg).__name__)
            else:
                alg_name = alg

            self.results[alg_name] = {}

            if verbose:
                logger.info("Running %s...", alg_name)

            for bench in self.useBenchmarks:
                if not isinstance(bench, "".__class__):
                    bench_name = str(type(bench).__name__)
                else:
                    bench_name = bench

                if verbose:
                    logger.info("Running %s algorithm on %s benchmark...", alg_name, bench_name)

                self.results[alg_name][bench_name] = []
                for _ in range(self.nRuns):
                    algorithm = AlgorithmUtility().get_algorithm(alg)
                    benchmark_stopping_task = self.benchmark_factory(bench)
                    self.results[alg_name][bench_name].append(algorithm.run(benchmark_stopping_task))
            if verbose:
                logger.info("---------------------------------------------------")
        if export == "dataframe":
            self.__export_to_dataframe_pickle()
        elif export == "json":
            self.__export_to_json()
        elif export == "xsl":
            self._export_to_xls()
        elif export == "xlsx":
            self.__export_to_xlsx()
        else:
            raise TypeError("Passed export type %s is not supported!", export)
        return self.results
