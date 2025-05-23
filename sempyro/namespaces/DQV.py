# Copyright 2024 Stichting Health-RI
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from rdflib import URIRef
from rdflib.namespace import DefinedNamespace, Namespace


class DQV(DefinedNamespace):
    """
    Namespace for the Data Quality Vocabulary

    Generated based on https://www.w3.org/TR/vocab-dqv/
    Date: 2025-05-13
    """

    hasQualityAnnotation: URIRef
    QualityCertificate: URIRef

    _NS = Namespace("http://www.w3.org/ns/dqv#")
